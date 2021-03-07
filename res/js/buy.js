(function () {
    let elms = document.querySelectorAll(".art-item button");
    for(let i = 0; i < elms.length; i++) {
        elms[i].addEventListener("click", function (ev) {
            let artItem = ev.target.parentElement.parentElement;
            let marketId = artItem.attributes["market-id"].value;

            fetch("/api/buy", {
              method: "POST",
              body: JSON.stringify({
                  "market_id": marketId,
              })
            }).then(()=>{
                location.reload();
            });
        });
    }
})();