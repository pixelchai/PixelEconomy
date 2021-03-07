(function () {
    let elms = document.querySelectorAll(".art-item button");
    for(let i = 0; i < elms.length; i++) {
        elms[i].addEventListener("click", function (ev) {
            let artItem = ev.target.parentElement.parentElement;
            let artId = artItem.attributes["art-id"].value;
            let price = parseInt(artItem.querySelector("input").value);

            fetch("/api/sell", {
              method: "POST",
              body: JSON.stringify({
                  "art_id": artId,
                  "price": price,
              })
            }).then(()=>{
                console.log("wow!!!");
            });
        });
    }
})();