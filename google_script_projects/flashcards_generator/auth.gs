/* auth function */

function auth() {
    try {
        var url = "http://kindledatabaseconverter.com/auth";
        var payload = {
            username: "sebastien",
            password: "RDvNifgjtJ6p1DA"
        };

        payload = JSON.stringify(payload);
        var options = {
            method: "post",
            contentType: "application/json",
            payload: payload
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        var data = JSON.parse(result);
        return data["access_token"]
    } catch (e) {
        Logger.log(e)
    }
}