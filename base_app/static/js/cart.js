
var allUpdateBtns = document.getElementsByClassName("update-cart")

for(i=0;i<allUpdateBtns.length; i++){
	allUpdateBtns[i].addEventListener("click",function(){
	var productId = this.dataset.product;
	var action = this.dataset.action;
		console.log("id:",productId,"action:",action)

	console.log("user:",user)
	if(user=="AnonymousUser"){
		console.log("user not logged in")
	}
	else{
		UpdateCartItem(productId,action);
	}

	});
function UpdateCartItem(productId,action){
	console.log("user is logged in, sending data");

	var url = "/update_cart/";

	fetch(url,{
		method:'POST',
		headers:{
			"Content-Type":"application/json",
			"X-CSRFToken":csrftoken,
		},

		body:JSON.stringify({"productId":productId,"action":action})
	})

	.then((response)=>{
		return response.json()
	})
	.then((data)=>{
		console.log("data:",data)
		location.reload()
	})	
}
	
}