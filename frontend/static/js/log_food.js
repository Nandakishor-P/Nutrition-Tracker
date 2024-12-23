// JavaScript to dynamically add food item input fields
function addFoodItem() {
  const container = document.getElementById('food-items-container');
  const numItems = document.getElementById('num_items').value || 0;

  // Clear existing inputs to avoid duplication
  container.innerHTML = '';

  for (let i = 0; i < numItems; i++) {
    const input = document.createElement('input');
    input.type = 'text';
    input.name = `food_item_${i + 1}`;
    input.placeholder = `Food Item ${i + 1}`;
    input.required = true; // Make it required
    container.appendChild(input);
  }
}
