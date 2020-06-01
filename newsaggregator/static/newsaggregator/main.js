document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('.readLater').forEach(button => {
  button.onclick = () => {
    const request = new XMLHttpRequest();
    link  = button.value;
    title = button.getAttribute('data-title');
    request.open('GET', `/readLater?link=${link}&title=${title}`);
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data["success"] == true){
      alert("news added in saved news, Visit your proofile to read it later");
      }
    };
    // Send request
    request.send();
  };
  });

document.querySelectorAll('.category').forEach(button => {
button.onclick = () => {
    category = button.getAttribute('data-cat');
    console.log("category defined in html (before on click)" + category)
    if (button.innerHTML == category)
        followCategory(category);

else{
    unfollowCategory(category);
}


};
});
document.querySelector('#changepasswordbutton').onclick = () => {
  div = document.querySelector('#changepasswordfields');
  cancel = document.querySelector('#cancel');
  cancel.onclick = () => {
    div.hidden = true;
  };

  div.hidden = false;
};
});

function followCategory(category){
  const request = new XMLHttpRequest();
  console.log("category inside follow category function"+ category);
  request.open('GET', `/followCategory/${category}`);
  request.onload = () => {
    const data = JSON.parse(request.responseText);
    if (data["success"] == true){
      b = document.querySelector(`[data-cat = ${category}]`);
      console.log("inner html"+b.innerHTML);
      b.innerHTML = b.innerHTML + '&#10003;';
      b.onclick = () => {
        unfollowCategory(category);
      };
    }
  };
  request.send();
}

function unfollowCategory(category){
  const request = new XMLHttpRequest();
  request.open('GET', `/unfollowCategory/${category}`);
  request.onload = () => {
    const data = JSON.parse(request.responseText);
    if (data["success"] == true){
      b =   document.querySelector(`[data-cat = ${category} ]`);
      b.innerHTML  = category;
      b.onclick = () =>{
        followCategory(category);
      }
  };
}
  request.send();
}
