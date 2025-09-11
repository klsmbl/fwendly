# Fwendly Conwection — Complete (Tailwind + Pagination + Friends + Testimonials + Search)

This is the full ready-to-run project with:
- Auth & profiles (Django Allauth + Profile)
- Friends (friend requests, accept/remove)
- Testimonials (post and view testimonials)
- Search (username/location/interests)
- Tailwind-like precompiled CSS bundled at `static/css/tailwind.css`
- Modern card UI and pagination for lists

## Quickstart
1. Create & activate virtualenv
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Apply migrations & create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```
4. Run the server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/

Notes:
- Email backend prints to console for dev.
- Tailwind is precompiled (light-mode only). You can replace `static/css/tailwind.css` with a real Tailwind build later if desired.
