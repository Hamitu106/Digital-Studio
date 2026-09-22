#!/data/data/com.termux/files/usr/bin/bash

clear

echo "========================================"
echo "🔍 DIGITAL STUDIO ADMIN CHECK"
echo "========================================"

echo

echo "📁 فایل‌ها:"
echo

if [ -f index.html ]; then
    echo "✅ index.html"
else
    echo "❌ index.html پیدا نشد"
fi

if [ -f private.html ]; then
    echo "✅ private.html"
else
    echo "❌ private.html پیدا نشد"
fi

echo
echo "----------------------------------------"
echo "🔎 بررسی private.html"
echo "----------------------------------------"

grep -q "crypto.randomUUID" private.html \
    && echo "✅ ساخت توکن تصادفی" \
    || echo "❌ ساخت توکن تصادفی پیدا نشد"

grep -q "device_token" private.html \
    && echo "✅ ارسال device_token" \
    || echo "❌ ارسال device_token پیدا نشد"

grep -q "admin_access" private.html \
    && echo "✅ اتصال به admin_access" \
    || echo "❌ اتصال به admin_access پیدا نشد"

grep -q "127.0.0.1:8080" private.html \
    && echo "✅ آدرس localhost وجود دارد" \
    || echo "⚠️ آدرس localhost وجود ندارد"

echo
echo "----------------------------------------"
echo "🔎 بررسی index.html"
echo "----------------------------------------"

grep -q "admin_token" index.html \
    && echo "✅ دریافت admin_token" \
    || echo "❌ دریافت admin_token پیدا نشد"

grep -q "admin_access" index.html \
    && echo "✅ اتصال به admin_access" \
    || echo "❌ اتصال به admin_access پیدا نشد"

grep -q "device_token" index.html \
    && echo "✅ بررسی device_token" \
    || echo "❌ بررسی device_token پیدا نشد"

grep -q "expires_at" index.html \
    && echo "✅ بررسی expires_at" \
    || echo "❌ بررسی expires_at پیدا نشد"

grep -q "digitalStudioIsAdmin" index.html \
    && echo "✅ سیستم فعال‌سازی Admin" \
    || echo "❌ سیستم فعال‌سازی Admin پیدا نشد"

echo
echo "----------------------------------------"
echo "🌐 بررسی localhost"
echo "----------------------------------------"

if curl -s --max-time 3 \
    http://127.0.0.1:8080/ \
    >/dev/null
then
    echo "✅ localhost:8080 فعال است"
else
    echo "❌ localhost:8080 فعال نیست"
fi

echo
echo "========================================"
echo "🏁 بررسی تمام شد"
echo "========================================"
