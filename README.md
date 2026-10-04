# STEP Blog - Dərs 8 (bütün səhifələr template-də)

Bu layihə göndərilmiş `Step_Django_2-main` layihəsi üzərində hazırlanıb.
Dərs 8-in 7 əsas tapşırığı və 2 bonusu yerinə yetirilib.

## Başlatmaq

Python **3.13+** və [`uv`](https://docs.astral.sh/uv/) quraşdırılmış olmalıdır.

```bash
uv sync --locked
uv run python manage.py migrate
uv run python manage.py runserver
```

Brauzerdə `http://127.0.0.1:8000/` aç. Test üçün:

```bash
uv run python manage.py check
uv run python manage.py test blog
```

## Ünvanlar

| Ünvan | Nə göstərir |
| --- | --- |
| `/` və `/posts/` | Bütün postlar; ana səhifə |
| `/posts/1/` | Postun detalları və söz sayı |
| `/author/murad/` | Müəllifin 2 postu |
| `/author/xyz/` | 200 və boş siyahı mesajı |
| `/categories/` | 3 kateqoriya |
| `/categories/oyunlar/` | Kateqoriyanın postları |
| `/latest/` | Son 3 post, sıra nömrəsi, tarix |
| `/stats/` | 5 post və 3 kateqoriya |
| `/about/` | Haqqımızda |
| `/contact/` | Əlaqə |

`templates/base.html` ümumi başlıq, navbar, CSS, footer və JS-i ehtiva edir.
`templates/partials/navbar.html` menyudur, `templates/partials/_post_card.html`
isə bütün kart siyahılarında istifadə edilir. Bütün daxili keçidlər `{% url %}`
ilə yazılıb. `blog/views.py` yalnız `render()` istifadə edir (mövcud olmayan
post/kateqoriya üçün `Http404` istisnası istisna olmaqla).

**Qeyd:** Əlaqə səhifəsindəki `info@example.com` və `+994 50 123 45 67`
**nümunə** məlumatlardır. Öz əlaqə məlumatlarınla əvəz et.

**Təhvil:** Müəllim eyni mövcud `step-blog` reposunu və hər tapşırıq üçün ayrı
commit tələb edir. Buradakı ZIP sənin mövcud GitHub reponu dəyişmir.
`git-patches/` qovluğunda ardıcıl tətbiq oluna bilən lokal commit patch-ləri var.
Onları mövcud repoya tətbiq etməzdən əvvəl öz dəyişikliklərinlə uyğunluğu
yoxla. `.venv/`, `__pycache__/` və `db.sqlite3` `.gitignore`-a salınıb.
