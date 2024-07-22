function sendTelegramWebData(url) {
    const initData = Telegram.WebView.initParams.tgWebAppData;
    const encodedInitData = encodeURIComponent(initData);

    let newUrl = `${url}?init_data=${encodedInitData || ''}`;

    window.location.href = newUrl;
}