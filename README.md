# 👥 Git Standup

Bir git reposunda belirli bir zaman aralığında kimin neler yaptığını
özetleyen komut satırı aracı. Günlük standup toplantılarında "dün ne
yaptım" sorusuna hızlıca cevap vermek veya takım aktivitesini gözden
geçirmek için kullanışlıdır.

## Özellikler

- 📅 Esnek zaman aralığı (`yesterday`, `1 week ago`, belirli tarihler)
- 👤 Varsayılan olarak sadece mevcut git kullanıcısının commit'lerini gösterir
- 👥 `--all-authors` ile tüm takımın commit'lerini yazara göre gruplu gösterir
- 📊 Her commit için satır ekleme/silme ve değişen dosya sayısı
- 🚫 Harici bağımlılık yok — sadece sistemde kurulu `git` komutunu kullanır

## Kurulum

Sistemde `git` kurulu olması yeterlidir, ek bir Python paketi gerekmez.

## Kullanım

```bash
# Bugün ne yaptım? (mevcut git kullanıcısı, gece yarısından itibaren)
python3 git_standup.py

# Dünden bugüne
python3 git_standup.py --since yesterday

# Son 1 hafta
python3 git_standup.py --since "1 week ago"

# Belirli bir tarih aralığı
python3 git_standup.py --since "2024-01-01" --until "2024-01-31"

# Tüm takımı göster (sadece kendi commit'lerin değil)
python3 git_standup.py --since yesterday --all-authors

# Belirli bir kişiyi filtrele
python3 git_standup.py --since "1 month ago" --author "Ayşe"

# Başka bir repo için çalıştır
python3 git_standup.py --repo /yol/baska/proje --since yesterday
```

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| `--repo` | Git reposu yolu | mevcut klasör |
| `--since` | Başlangıç zamanı | `midnight` (bugün) |
| `--until` | Bitiş zamanı | şimdi |
| `--author` | Belirli bir yazarı filtrele | — |
| `--all-authors` | Sadece mevcut kullanıcı yerine herkesi göster | kapalı |

## Örnek çıktı

```
============================================================
Ayşe Yılmaz  —  3 commit
  +145 / -23 satır, 5 dosya değişikliği
------------------------------------------------------------
  [a1b2c3d4] 2024-01-15 09:32  Kullanıcı kimlik doğrulama eklendi
    +89 / -2  (3 dosya)
  [e5f6g7h8] 2024-01-15 11:05  Test coverage artırıldı
    +56 / -21  (2 dosya)
```

## Lisans

MIT


---

> Made in [discord.gg/codeshare](https://discord.gg/codeshare) · [astra-dev.com.tr](https://astra-dev.com.tr)
