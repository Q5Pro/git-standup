"""
Git Standup
============
Bir git reposunda belirli bir zaman aralığında kimin neler yaptığını
özetler. Günlük "standup" toplantılarında "dün ne yaptım" sorusuna
cevap vermek, ya da takım aktivitesini takip etmek için kullanışlıdır.

Kullanım:
    python git_standup.py                          # Bugünkü commit'ler (mevcut kullanıcı)
    python git_standup.py --since yesterday          # Dünden bugüne
    python git_standup.py --since "1 week ago"        # Son 1 hafta
    python git_standup.py --all-authors               # Tüm katkıcıları göster
    python git_standup.py --author "Ayşe"             # Belirli bir kişiyi filtrele
    python git_standup.py --repo /yol/baska/repo       # Başka bir repo için çalıştır
    python git_standup.py --since "2024-01-01" --until "2024-01-31"

Not: Bu script, sistemde kurulu olan 'git' komutunu kullanır;
GitPython gibi ek bir kütüphane gerekmez.
"""

import argparse
import subprocess
import sys
from collections import defaultdict


def run_git(args: list, cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + args, cwd=cwd, capture_output=True, text=True, check=True
        )
        return result.stdout
    except FileNotFoundError:
        print("Hata: 'git' komutu bulunamadı. Git kurulu mu?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Git komutu başarısız oldu: {e.stderr.strip()}")
        sys.exit(1)


def get_current_user(repo: str) -> str:
    name = run_git(["config", "user.name"], repo).strip()
    return name


def get_log(repo: str, since: str, until: str, author: str = None) -> list:
    """Git log'u parse edilebilir bir formatta çeker.
    Format: hash|author|date|subject, ardından değişen dosyalar."""
    log_args = [
        "log",
        f"--since={since}",
        "--pretty=format:COMMIT|%H|%an|%ad|%s",
        "--date=format:%Y-%m-%d %H:%M",
        "--numstat",
    ]
    if until:
        log_args.insert(1, f"--until={until}")
    if author:
        log_args.append(f"--author={author}")

    output = run_git(log_args, repo)
    return parse_log_output(output)


def parse_log_output(output: str) -> list:
    commits = []
    current = None

    for line in output.splitlines():
        if line.startswith("COMMIT|"):
            if current:
                commits.append(current)
            _, commit_hash, author, date, subject = line.split("|", 4)
            current = {
                "hash": commit_hash[:8],
                "author": author,
                "date": date,
                "subject": subject,
                "files_changed": 0,
                "additions": 0,
                "deletions": 0,
            }
        elif line.strip() and current is not None:
            parts = line.split("\t")
            if len(parts) == 3:
                added, removed, _ = parts
                current["files_changed"] += 1
                current["additions"] += int(added) if added.isdigit() else 0
                current["deletions"] += int(removed) if removed.isdigit() else 0

    if current:
        commits.append(current)

    return commits


def group_by_author(commits: list) -> dict:
    grouped = defaultdict(list)
    for commit in commits:
        grouped[commit["author"]].append(commit)
    return grouped


def print_summary(grouped: dict):
    if not grouped:
        print("Belirtilen zaman aralığında hiçbir commit bulunamadı.")
        return

    for author, commits in grouped.items():
        total_additions = sum(c["additions"] for c in commits)
        total_deletions = sum(c["deletions"] for c in commits)
        total_files = sum(c["files_changed"] for c in commits)

        print(f"\n{'=' * 60}")
        print(f"{author}  —  {len(commits)} commit")
        print(f"  +{total_additions} / -{total_deletions} satır, {total_files} dosya değişikliği")
        print(f"{'-' * 60}")

        for commit in commits:
            print(f"  [{commit['hash']}] {commit['date']}  {commit['subject']}")
            print(f"    +{commit['additions']} / -{commit['deletions']}  ({commit['files_changed']} dosya)")


def main():
    parser = argparse.ArgumentParser(description="Git commit'lerini standup özeti olarak gösterir")
    parser.add_argument("--repo", type=str, default=".", help="Git reposu yolu (varsayılan: mevcut klasör)")
    parser.add_argument("--since", type=str, default="midnight", help="Başlangıç zamanı (örn. 'yesterday', '1 week ago', '2024-01-01')")
    parser.add_argument("--until", type=str, default=None, help="Bitiş zamanı")
    parser.add_argument("--author", type=str, default=None, help="Belirli bir yazarı filtrele")
    parser.add_argument("--all-authors", action="store_true", help="Sadece mevcut kullanıcı yerine herkesi göster")
    args = parser.parse_args()

    author_filter = None if args.all_authors else (args.author or get_current_user(args.repo))

    if author_filter:
        print(f"Yazar filtresi: {author_filter}  (tümünü görmek için --all-authors kullanın)")
    print(f"Zaman aralığı: {args.since}{' - ' + args.until if args.until else ' - şimdi'}\n")

    commits = get_log(args.repo, args.since, args.until, author_filter)
    grouped = group_by_author(commits)
    print_summary(grouped)


if __name__ == "__main__":
    main()
