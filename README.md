# Health_diet :poultry_leg:	:green_salad:	:pizza:	

## Description

Simple calorie and PFC (proteins, fats, carbohydrates) tracking web application that I made to learn new technologies. 

## Functionality
<details>
  
  <summary>User should create an account to start using application. <br/> Click to see screens of 'Create account' and 'Login' pages!</summary>
  
  > ![create_account](https://user-images.githubusercontent.com/81222865/168161101-6874b1d2-f384-42ba-b53e-cba3b28b99dc.jpg)
  > ![login](https://user-images.githubusercontent.com/81222865/168161247-a763265e-b630-4581-bddc-127d9f49bc7f.jpg)

</details>

<details>
  
  <summary>User can access food calorie table and dicsover the caloric content for common russian foods.<br/>Click to see screen of calories table!</summary>
  
  > ![PFC_table](https://user-images.githubusercontent.com/81222865/168161318-7c37cf26-d266-4bd1-8f13-39a089df3438.jpg)

</details>

<details>
  
  <summary>User can add information on food consumed (type of product, product, amount and meal) to check on calories.<br/>Click to see screen of page with adding info to the diary!</summary>
  
  > ![add_to_diary](https://user-images.githubusercontent.com/81222865/168161437-a149cf38-4a4d-44c8-a710-bc9e4d093df4.jpg)

</details>

<details>

  <summary>User can get statistics on food consumed and PFC for selected day.<br/>Click to see screen of page with stats on PFC and types of food for selected day!</summary>
  
  > ![show_stats](https://user-images.githubusercontent.com/81222865/168161478-490c7161-3aff-4b16-bf4a-15ebd598fe12.jpg)

</details>

## Technologies used
* <a href='https://www.python.org/'>Python3.10</a> (Flask, sqlite3, pandas, plotly and other libraries)
* HTML
* CSS
* <a href='https://getbootstrap.com/'>Bootstrap</a>
* <a href='https://www.docker.com/'>Docker</a>
* SQL

## Usage
### Method 1 (using Docker) :package:	:whale:	
* Clone this repo
* Run **`docker-compose up`**
* Enter in browser **`http://localhost:8000/`**
* Don't forget to remove container and image after exiting the program (**`docker rm [container_name]`** and **`docker image rm [image_name]`** )

### Method 2 (without Docker)
* Clone this repo
* Install all necessary packages (see file requirements.txt)
* run **`app.py`**

*P.s. there is already test user info in databases (email: test@gmail.com, password: test).*
