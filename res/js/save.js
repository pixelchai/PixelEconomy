(function () {
    document.querySelector(".pixelart .meta button").addEventListener("click", function(){
        let title = document.querySelector(".pixelart .meta .title-input").value;
        fetch("/api/save", {
          method: "POST",
          body: JSON.stringify({
              "title": title,
              "data": getData(),
          })
        });
    });
})();