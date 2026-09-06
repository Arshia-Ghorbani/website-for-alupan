from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

# ---------------------------------------------------------------------------
# ⚠ PLACEHOLDER MARKETING COPY
# Every figure below (Uf values, cycle counts, Pa ratings, project areas) is a
# stand-in so the layout can be evaluated. Replace each one with a number you
# can support from an AluK datasheet or your own test certificate before this
# page goes live — publishing unverified performance claims for a construction
# product is a liability, not a typo.
#
# Once the systems/projects apps have real rows, swap these literals for
# querysets:  System.objects.published()[:6]  /  Project.objects.published()
# ---------------------------------------------------------------------------

HOMEPAGE_STATS = [
    {"value": 25, "suffix": "+", "label": _("سال تجربه در صنعت نما")},
    {"value": 120000, "suffix": " م²", "label": _("نمای اجراشده")},
    {"value": 450, "suffix": "+", "label": _("پروژه‌ی تکمیل‌شده")},
    {"value": 9, "suffix": "", "label": _("استان تحت پوشش")},
]

TECH_STEPS = [
    {
        "index": "۰۱",
        "title": _("پروفیل ترمال‌بریک"),
        "body": _(
            "نوار پلی‌آمید تقویت‌شده مسیر انتقال حرارت میان جداره‌ی داخلی و "
            "خارجی پروفیل را قطع می‌کند؛ نتیجه، کاهش بار سرمایشی و حذف "
            "میعان روی قاب در زمستان است."
        ),
        "specs": [(_("عرض ترمال بریک"), "24 mm"), (_("ضریب Uf"), "1.4 W/m²K")],
    },
    {
        "index": "۰۲",
        "title": _("یراق‌آلات مهندسی‌شده"),
        "body": _(
            "لولا، قفل و مکانیزم بازشو از همان سیستم AluK تأمین می‌شوند، پس "
            "بار وزن بازشو روی نقاطی می‌نشیند که پروفیل برای آن طراحی شده."
        ),
        "specs": [(_("تست چرخه"), "25,000 cycles"), (_("حداکثر وزن لنگه"), "160 kg")],
    },
    {
        "index": "۰۳",
        "title": _("آب‌بندی سه‌مرحله‌ای"),
        "body": _(
            "سه خط واشر EPDM با محفظه‌ی تخلیه‌ی فشار میان آن‌ها، آب نفوذی را "
            "پیش از رسیدن به جداره‌ی داخلی جمع و به بیرون هدایت می‌کند."
        ),
        "specs": [(_("نفوذ آب"), "1200 Pa"), (_("بار باد"), "2400 Pa")],
    },
]

SYSTEM_PARTS = [
    {"index": "۰۱", "icon": "profile",  "title": _("پروفیل آلومینیوم"),
     "text": _("آلیاژ 6063-T6، اکستروژن با تلورانس EN 12020.")},
    {"index": "۰۲", "icon": "break",    "title": _("ترمال بریک پلی‌آمید"),
     "text": _("نوار PA66 با ۲۵٪ الیاف شیشه، غلتک‌خورده در پروفیل.")},
    {"index": "۰۳", "icon": "hardware", "title": _("یراق‌آلات"),
     "text": _("لولا، قفل چندنقطه‌ای و مکانیزم بازشوی کنترل‌شده.")},
    {"index": "۰۴", "icon": "gasket",   "title": _("واشر و درزگیر"),
     "text": _("EPDM اکسترود‌شده، پایدار در برابر UV و نوسان دما.")},
    {"index": "۰۵", "icon": "glass",    "title": _("شیشه‌ی دوجداره"),
     "text": _("لوایمیسیو با اسپیسر گرم و پرشدگی آرگون.")},
    {"index": "۰۶", "icon": "anchor",   "title": _("اتصالات سازه‌ای"),
     "text": _("براکت قابل تنظیم در سه محور برای جذب رواداری سازه.")},
]


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            stats=HOMEPAGE_STATS,
            tech_steps=TECH_STEPS,
            parts=SYSTEM_PARTS,
        )
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


def healthz(request) -> JsonResponse:
    """Liveness probe used by Docker/compose healthchecks and load balancers."""
    return JsonResponse({"status": "ok"})


def readyz(request) -> HttpResponse:
    """Readiness probe: verifies the database is actually reachable."""
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:  # noqa: BLE001
        return JsonResponse({"status": "database unavailable"}, status=503)
    return JsonResponse({"status": "ready"})


# --- error handlers --------------------------------------------------------
def bad_request(request, exception=None):
    return render(request, "errors/400.html", status=400)


def permission_denied(request, exception=None):
    return render(request, "errors/403.html", status=403)


def page_not_found(request, exception=None):
    return render(request, "errors/404.html", status=404)


def server_error(request):
    return render(request, "errors/500.html", status=500)
