document.addEventListener("DOMContentLoaded", function(){
    const input = document.getElementById("customer");
    const hiddenId = document.getElementById("customer_id");
    const suggestionsDiv = document.getElementById("suggestions");

    input.addEventListener("input", function(){
        const query = input.value;

        if(query.length === 0){
            suggestionsDiv.innerHTML = "";
            hiddenId.value = ""; 
            return;
        }

        fetch(`/autocomplete?customer=${query}`)
            .then(response => response.json())
            .then(data => {
                const results = data.matching_results;
                suggestionsDiv.innerHTML = "";

                results.forEach(cust => {
                    const div = document.createElement("div");
                    div.textContent = cust.name; 
                    div.classList.add("cursor-pointer", "hover:bg-gray-300", "p-2");
                    div.addEventListener("click", () => {
                        input.value = cust.name;    
                        hiddenId.value = cust.id; 
                        suggestionsDiv.innerHTML = "";
                    });
                    suggestionsDiv.appendChild(div);
                });
            });
    });
});
