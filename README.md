<img align="left" height="70" src="./assets/logo/logo_nobg.png" />

# Pizza chart

Pie chart, with a salty twist.

> [!IMPORTANT] 
> The purpose of this repository is to create a fun data visualization representing the preferred pizzas during pizza days at work. Icons used in this project are sourced from Flaticon and credited according to Flaticon’s attribution guidelines, which are listed in the [AUTHORS.md](./assets/AUTHORS.md) file.
> <br>These assets are used strictly for recreational purposes. If the content infringes on any rights or you would like it removed, please reach out, and it will be promptly taken down.

<!-- Adaptation to color scheme taken from https://stackoverflow.com/questions/65413712/changing-readme-md-image-display-conditional-to-github-light-mode-dark-mode -->
<br />
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Luca-Pozzi/pizza_chart/raw/master/assets/charts/summary_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/Luca-Pozzi/pizza_chart/raw/master/assets/charts/summary_light.png">
  <img alt="Summary charts of pizza days at WE-COBOT in either dark or light mode adapting to selected color scheme" src="./assets/charts/summary_dark.png">
</picture>
<br />

## How to use

### Add a pizza
When a new pizza is added to the database, the corresponding image can be created using the [pizza_maker.ipynb](pizza_maker.ipynb) notebook. Run the notebook following the *How to use* instructions to compose and save your pizza.

### Add a topping
If the topping for your pizza is not available in the [toppings](./assets/toppings/) folder, you can add a proper PNG image, with the following procedure:
* find a suitable icon/drawing/illustration. [Flaticon](https://www.flaticon.com/) is the preferred source, but any image will do, provided that it comes with a license allowing redistribution.
* save the image with a meaningful name in the [toppings](./assets/toppings/) folder.
* add the acknowledgment to the authors in the [AUTHORS.md](./assets/AUTHORS.md) file.

### Plot
Pizza charts can be plotted via the [pizza_chart_example.ipynb](pizza_chart_example.ipynb) notebook.

### Report
Data collected during pizza days at [Politecnico di Milano - Polo Territoriale di Lecco](https://www.polo-lecco.polimi.it/) are available in [data.xlsx](./data/data.xlsx) Excel file.
The [`pizza_report.py`](./pizza_report.py) gathers data from the Excel file to generate summary charts regarding our pizza days. 
The updated summary is displayed at the top of this [`README`](README.md). Individual charts are available in [`assets/charts`](./assets/charts/).

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](LICENSE).

You are free to share and adapt the material for non-commercial purposes, as long as you provide appropriate credit. You can attribute this project as
```
[Pizza chart](https://github.com/Luca-Pozzi/pizza_chart)
```

## Author
* Luca :envelope: [luca6.pozzi@mail.polimi.it](mailto:luca6.pozzi@mail.polimi.it)
