# Pizza chart

Pie chart, with a salty twist.

> [!IMPORTANT] 
> The purpose of this repository is to create a fun data visualization representing the preferred pizzas during pizza days at work. Icons used in this project are sourced from Flaticon and credited according to Flaticon’s attribution guidelines, which are listed in the [AUTHORS.md](./assets/AUTHORS.md) file.
> <br>These assets are used strictly for recreational purposes. If the content infringes on any rights or you would like it removed, please reach out, and it will be promptly taken down.

## How to use

### Add a pizza
When a new pizza is added to the database, the corresponding image can be created using the [pizza_maker.ipynb](pizza_maker.ipynb) notebook. Run the notebook following the *How to use* instructions to compose and save your pizza.

### Add a topping
If the topping for your pizza is not available in the [toppings](./assets/toppings/) folder, you can add a proper PNG image, with the following procedure:
* find a suitable icon/drawing/illustration. [Flaticon](https://www.flaticon.com/) is the preferred source, but any image will do, provided that it comes with a license allowing redistribution.
* save the image with a meaningful name in the [toppings](./assets/toppings/) folder.
* add the acknowledgment to the authors in the [AUTHORS.md](./assets/AUTHORS.md) file.

### Plot
Pizza charts can be plotted via the [pizza_chart.ipynb](pizza_chart.ipynb) notebook.

### Report
Data collected during pizza days at [Politecnico di Milano - Polo Territoriale di Lecco](https://www.polo-lecco.polimi.it/) are available in [data.xlsx](./data/data.xlsx) Excel file.
The [`pizza_report.py`](./pizza_report.py) is under development (:construction_worker:). It gathers data from the Excel file to generate a Markdown summary of relevant stats regarding our pizza days.

## Author
* Luca :envelope: [luca6.pozzi@mail.polimi.it](mailto:luca6.pozzi@mail.polimi.it)