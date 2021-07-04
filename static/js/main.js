var selected_store_list = [];

function toggleSelectStoreButton(store_name) {
    if (store_name == "SevenEleven") {
        var store_btn = $("#select-seven-btn-id");
    } else if (store_name == "FamilyMart") {
        var store_btn = $("#select-famima-btn-id");
    }
    if (store_btn.val() == "on") {
        // リストからstore_nameを削除する
        selected_store_list.splice(selected_store_list.indexOf(store_name), 1);
        store_btn.removeClass("active");
        store_btn.val("off");
    } else {
        selected_store_list.push(store_name);
        store_btn.addClass("active");
        store_btn.val("on");
    }
    console.log(selected_store_list);
}
toggleSelectStoreButton("SevenEleven");
toggleSelectStoreButton("FamilyMart");

$("button").click(function() {
    toggleSelectStoreButton(this.outerText);
});

// TODO: 店舗の近さでソートする。google mapで距離をとる
// TODO: bootstrapで見た目をカッコよくする。
// TODO: ローソンの商品のスクレイピングをする。
// TODO: 麺 -> パスタ、うどん、ラーメン、冷やし中華を調べる。
jQuery(function($) {
    $(document).ajaxSend(function() {
        $("#overlay").fadeIn(300);
    });
});
var geolocation_is_available = false;

function CreateGoogleMapUrl(userLat, userLon, storeLat, storeLon) {
    return (
        "https://www.google.com/maps/dir/?api=1&origin=" +
        userLat +
        "," +
        userLon +
        "&destination=" +
        storeLat +
        "," +
        storeLon
    );
}

// Set lat lon after page loading
if (navigator.geolocation) {
    // user's mobile is available to use geolocation.
    var geolocation_is_available = true;
    var is_getting_coordinate = false;
    navigator.geolocation.getCurrentPosition(success, fail);
} else {
    // user's mobile is not available to use geolocation.
    alert("あなたの端末では現在位置を取得できません。");
}

function success(pos) {
    document.getElementById("lat").value = pos.coords.latitude;
    document.getElementById("lon").value = pos.coords.longitude;
    console.log("位置情報の取得を完了しました。");
    $("#status").text("位置情報の取得を完了しました。");
    is_getting_coordinate = true;
}

function fail(pos) {
    console.log("位置情報の取得に失敗しました。エラーコード：");
}

$("#btn").on("click", function() {
    if (!geolocation_is_available || !is_getting_coordinate) {
        alert("現在位置情報を取得しています....　2,3秒お待ちください。");
        return false;
    }
    productName = document.getElementById("name").value;
    userLat = parseFloat(document.getElementById("lat").value);
    userLon = parseFloat(document.getElementById("lon").value);
    var jsonData = JSON.stringify({
        ProductName: productName,
        UserLat: userLat,
        UserLon: userLon,
    });
    console.log("send data to server: " + jsonData);
    $.ajax({
            url: "/search",
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: jsonData,
            cache: true,
            timeout: 60000,
        })
        .done(function(results) {
            // テーブルのtbodyの部分を空にする
            $("#myTable > tbody").empty();

            // 検索中のローディング画面をセット
            setTimeout(function() {
                $("#overlay").fadeOut(300);
            }, 500);

            console.log("ajax successful");
            console.log("data from server: ", results);

            var hit_num = 0; // 表に表示する件数
            // 検索結果をテーブルに表示させる
            for (var i = 0; i < results.length; i++) {
                r = results[i];
                // ユーザーが選択した店のみを表示する。
                if (selected_store_list.indexOf(r.dealer) != -1) {
                    hit_num++;
                    googleMapUrl = CreateGoogleMapUrl(userLat, userLon, r.lat, r.lon);
                    $("#myTable > tbody").append(
                        "<tr><td>" +
                        hit_num +
                        "</td> <td>" +
                        r.productName +
                        "</td><td><a href=" +
                        r.url +
                        ' target="_blank"><img src=' +
                        r.imgUrl +
                        ' width="128" height="96"></a></td><td>' +
                        r.price +
                        "</td><td>" +
                        r.storename +
                        "</td><td><a href=" +
                        googleMapUrl +
                        ' target="_blank">Google Map</a></td></tr>'
                    );
                }
            }
            // 表を更新した後はアップデートしなければソートが機能しない。
            $("#myTable").trigger("update");

            // 検索結果の件数の表示
            $("#hit-num").text(hit_num + "件ヒットしました。");
            if (hit_num == 0) {
                $("#hit-num").text("ヒットした商品はありませんでした。");
                return false;
            }
        })
        .fail(function(data) {
            console.log("ajax fail.");
            console.log("data: ", data);
        });
    // 通常でのsubmit処理を無効にする
    return false;
});