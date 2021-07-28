# mattox_groceries_automation

This is meant to be a very light and funny weekend project that brings some automation to our household groceries based on the recipes we'll be cooking

To keep it simple, it is based on google spreadsheets

So far, we've got two main pieces of code:

* rascunho_cria_cardapios.ipynb: A sketch notebook for generating next weeks recipes and updating grocieries shop list and recipes calendar (@ cardapio_automatico spreadsheet)
* adiciona_receita.py: A script that will take a recipe from template_add_receita tab on base_dishes spreadsheet, make some data prep and save it on the right recipes database (also on base_dishes spreadsheet)
