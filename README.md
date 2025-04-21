# – Dinamik Python Quiz Uygulaması

"Python Quiz Uygulaması", gelişmiş Python konularını içeren, kullanıcı puanı tutan, tekrar oynanabilen, yüksek skorları listeleyen ve PythonAnywhere üzerinde barındırılan bir dinamik quiz uygulamasıdır.

---

## 🚀 Özellikler

- 👤 Kullanıcı oturumu (session) takibi
- ❓ 5 soruluk rastgele seçilen Python quiz'i
- 📊 Skor kaydı, yüksek skor listesi
- 💾 SQLAlchemy destekli veritabanı
- 🌐 PythonAnywhere üzerinde yayında

---

## ⚙️ Ortam Değişkenleri (`.env`)

Proje kök dizinine `.env` dosyası oluşturun:

```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=supersecretkey
DATABASE_URL=sqlite:////home/sen19/python_quiz_app/instance/quiz.db

Veritabanı Kurulumu:

Terminalde proje dizinine girin:

cd /home/sen19/python_quiz_app


flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Proje Yapısı

python_quiz_app/
│
├── app.py
├── .env
├── instance/
│   └── quiz.db
├── flask_quiz_app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── routes.py
│   ├── models.py
│   └── templates/
│       ├── index.html
│       ├── quiz_form.html
│       ├── result.html
│       └── scores.html
├── migrations/
│   └── ... (otomatik oluşturulur)
└── README.md

PythonAnywhere'de WSGI ayarı:

# /var/www/sen19_pythonanywhere_com_wsgi.py

import sys
sys.path.insert(0, '/home/sen19/python_quiz_app')

from flask_quiz_app import create_app
application = create_app()
