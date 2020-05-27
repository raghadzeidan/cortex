{%block javascript%}
// Get references to the dom elements
var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');

var counter = 0;



function loadItems() {

  // Use fetch to request data and pass the counter value in the QS
  fetch(`/load/users/{{username}}?c=${counter}`).then((response) => {

    // Convert the response data to JSON
    response.json().then((data) => {

      // If empty JSON, exit the function
      if (!data.length) {

        // Replace the spinner with "No more posts"
        sentinel.innerHTML = "No more snapshots";
        return;
      }

      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {
		console.log(i)
        //> Clone the HTML template
        let template_clone = template.content.cloneNode(true);

        // Query & update the template content
        template_clone.querySelector("#title").innerHTML = `${data[i]['datetime']}`;
        template_clone.querySelector("#content").innerHTML = `${data[i]['pose']}`+ "<h3>`${data[i]['depth_image']}`</h3>"+`${data[i]['color_image']}`;
		console.log(5)
		var hunger = `${data[i]['feelings']['hunger']}` / 1;
		console.log(hunger);
		var thirst = `${data[i]['feelings']['thirst']}` / 1;
		var exh = `${data[i]['feelings']['exhaustion']}` / 1;
		
		var hunger_html = "<div id= \"hunger_feeling_bar\" class=\"progress-bar progress-bar-striped bg-warning\" role=\"progressbar\" style=\"width: 10%\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-valuenow= \"80\"></div>"
		var thirst_html = "<div id= \"thirst_feeling_bar\" class=\"progress-bar progress-bar-striped bg-succeed\" role=\"progressbar\" style=\"width: 10%\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-valuenow= " + thirst +"></div>"
		var exh_html = "<div id= \"exh_feeling_bar\" class=\"progress-bar progress-bar-striped bg-danger\" role=\"progressbar\" style=\"width: 10%\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-valuenow= " + exh +"></div>"

		template_clone.querySelector("#hunger_progress").append(hunger_html);
		//template_clone.querySelector("#exhaustion_feeling_bar").aria-valuenow = thirst;
		//template_clone.querySelector("#thirst_feeling_bar").aria-valuenow = exh;
		
        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;

        // Update the counter in the navbar
        //loaded.innerText = `${counter} items loaded`;

      }
    })
  })
}











// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {


  // If intersectionRatio is 0, the sentinel is out of view
  // and we don't need to do anything. Exit the function
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  //> Call the loadItems function
  loadItems();

});
	intersectionObserver.observe(sentinel)
{%endblock%}
