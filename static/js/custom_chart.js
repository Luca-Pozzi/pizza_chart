document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelector("#pizza-rows");
    const template = document.querySelector("#pizza-row-template");
    const addButton = document.querySelector("#add-pizza-row");

    if (!rows || !template || !addButton) {
        return;
    }

    function updateControls() {
        const pizzaRows = Array.from(rows.querySelectorAll(".pizza-row"));
        addButton.disabled = pizzaRows.length >= 20;
        pizzaRows.forEach((row) => {
            row.querySelector(".remove-pizza-row").disabled = pizzaRows.length === 1;
        });
    }

    addButton.addEventListener("click", () => {
        if (rows.querySelectorAll(".pizza-row").length >= 20) {
            return;
        }
        rows.appendChild(template.content.cloneNode(true));
        updateControls();
    });

    rows.addEventListener("click", (event) => {
        const button = event.target.closest(".remove-pizza-row");
        if (button && rows.querySelectorAll(".pizza-row").length > 1) {
            button.closest(".pizza-row").remove();
            updateControls();
        }
    });

    rows.addEventListener("change", (event) => {
        if (event.target.matches('select[name="pizza_visual"]')) {
            const option = event.target.selectedOptions[0];
            event.target.closest(".pizza-row").querySelector(".pizza-visual-preview").src =
                option.dataset.imageUrl;
        }
    });

    updateControls();
});
