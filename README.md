<img align="left" height="70" src="./assets/logo/logo.png" />

# Pizza chart

Pie charts, with a salty twist.

> [!NOTE] 
> The purpose of this repository is to create a fun data visualization representing the preferred pizzas during pizza days at work. 
> Data and the following summary stats refer to the pizza days at *Polo Territoriale di Lecco, Politecnico di Milano*.

<!-- Adaptation to color scheme taken from https://stackoverflow.com/questions/65413712/changing-readme-md-image-display-conditional-to-github-light-mode-dark-mode -->
<br />
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Luca-Pozzi/pizza_chart/raw/master/assets/charts/summary_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/Luca-Pozzi/pizza_chart/raw/master/assets/charts/summary_light.png">
  <img alt="Summary charts of pizza days at WE-COBOT in either dark or light mode adapting to selected color scheme" src="./assets/charts/summary_dark.png">
</picture>
<br />

More stats are available on [GitHub Pages](https://luca-pozzi.github.io/pizza_chart/).

---

## Table of contents
* [How to install](#how-to-install)
* [How to use](#how-to-use)
  * [Examples](#examples)
  * [Contribute]()

## How to install
1. Clone the repo
  ```
  git clone https://github.com/Luca-Pozzi/pizza_chart.git
  ```
2. Install the requirements (:warning: if you are working in a virtual environment, activate it first!)
  ```
  cd <path_to_pizza_chart>
  pip install -r requirements.txt
  ```

## How to use

> [!IMPORTANT]
> `pizza_chart` comes with built-in images included, which can be freely used for non-commercial purposes (see [license](./LICENSE)).
> In using `pizza_chart`, the user can also use contents from any source, including third-party images. **It is the user's responsibility to give proper attribution to the authors of said contents.**

### Examples
* [`pizza_chart.ipynb`](./examples/pizza_chart.ipynb)
<br>Demonstrates how to use the `pizza_chart.plot` function to visualize pizza orders as a custom pie chart. Shows how to specify your order and customize the chart’s appearance.

* [`pizza_maker.ipynb`](./examples/pizza_maker.ipynb)
<br>Lets you create new pizza images by combining base pizzas and toppings. Useful for generating assets for new pizza types, with interactive controls for customizing your pizza.

### Contribute
#### Add a pizza :pizza:
To add a new pizza to the assets, you have two main options:
* **Upload a picture.** Take a top-view picture of your pizza, ensuring that it is entirely visible.
Follow the tips in [ASSETS.md](./assets/ASSETS.md) to process it to the desired format, size and resolution.
* **Make a pizza with `pizza_maker.ipynb`.** See [_Examples_ section](#make-a-pizza-with-pizza_makeripynb).

#### Add a topping :tomato:
Get the picture of a topping by either:
* cropping a pizza from the images in [`assets/pizza`](./assets/pizzas)
* getting ingredients images from third-party sources ([Flaticon.com](https://www.flaticon.com/) is a great place to look, if you are down with a cartoonish style).

### Report
Data collected during pizza days at [Politecnico di Milano - Polo Territoriale di Lecco](https://www.polo-lecco.polimi.it/) are available in [data.xlsx](./data/data.xlsx) Excel file.
The [`pizza_report.py`](./pizza_report.py) gathers data from the Excel file to generate summary charts regarding our pizza days. 
The updated summary is displayed at the top of this [`README`](README.md). Individual charts are available in [`assets/charts`](./assets/charts/).

---

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](LICENSE).

You are free to share and adapt the material for non-commercial purposes, as long as you provide appropriate credit. You can attribute this project as
```
[Pizza chart](https://github.com/Luca-Pozzi/pizza_chart)
```

---

## Author
* Luca :envelope: [luca6.pozzi@mail.polimi.it](mailto:luca6.pozzi@mail.polimi.it)
