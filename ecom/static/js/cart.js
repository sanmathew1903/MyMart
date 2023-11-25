var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log(user);
    console.log("productId", productId, "Action", action);
  

  if (user === "AnonymousUser") {
    console.log("not logged in ");
  } else {
    console.log("daf");
    updateUserOrder(productId,action)
  }
});
}

function updateUserOrder(productId, action) {
  console.log("User logged in ");
  var url = "update_item";
  console.log(url)

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ 'productId': productId, 'action': action }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}
