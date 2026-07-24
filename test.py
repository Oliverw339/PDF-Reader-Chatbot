import PyPDF2 
from PyPDF2 import PdfReader
import sys

from PyPDF2 import PdfReader
from pathlib import Path

pdf_path = (
    Path(__file__).parent /
    "Baking PDFs" /
    "Keto-Breads-Digital-Version_Spreads_Upload (9).pdf"
)

reader = PdfReader(pdf_path)

print(type(reader))
print(type(reader.pages))
print(reader.pages)

"""
prompt: Give me a light and fluffy bread recipie
To make a light and fluffy grain-free bread, I'd recommend using the Classic Sandwich Loaf recipe as a base. Here's an adapted version:

**Light and Fluffy Grain-Free Bread Recipe**

YIELD: One 7.5” x 3.5” (19 x 9 cm) loaf (16 slices)

INGREDIENTS

DRY INGREDIENTS

* ½ cup sifted coconut flour (50 g)
* ¼ cup ground golden flaxseed (25 g)
* 1 tsp. baking soda (5 g)
* ½ tsp. sea salt (2.5 g)
* 1 tsp. tapioca flour (2.5 g)
* ¼ tsp. cream of tartar (1.25 g)
* 1 Tbsp. + 1 tsp. organic psyllium husk powder (12 g)

WET INGREDIENTS

* 3 large eggs
* 1 egg white
* 2 tbsp. apple cider vinegar
* ¼ cup hot water

ADDITIONAL INSTRUCTIONS

1. Preheat oven to 350°F (177°C).
2. Prepare the parchment sling as instructed in the Classic Sandwich Loaf recipe.
3. In a small bowl, combine the dry ingredients.
4. In another bowl, whisk together the eggs, egg white, apple cider vinegar, and hot water.
5. Add the dry ingredients to the wet ingredients and stir until combined.
6. Pour in additional hot water (about 1-2 tbsp.) if the batter is too thick.
7. Pour the batter into the prepared loaf pan and smooth the top.
8. Bake for 35-40 minutes, or until a toothpick inserted into the center comes out clean.

Tips to achieve a light and fluffy texture:

* Use room temperature eggs for better emulsification.
* Don't overmix the batter, as this can lead to a dense bread.
* Add more hot water if needed to achieve a thick but pourable consistency.
* Bake at the correct temperature to prevent burning or undercooking.

This adapted recipe should yield a light and fluffy grain-free bread with a slightly denser texture than traditional bread. Enjoy!

"""

"""
prompt: What ise th difference between sweet and savoury bread?

answer: The main difference between sweet and savory bread lies in the type of ingredients used, particularly in terms of flavorings, spices, and sweeteners.

Sweet breads typically contain added sugars, such as honey, maple syrup, or sugar, which give them a sweeter taste. They may also include fruits, nuts, or other sweet ingredients to enhance their flavor. Examples of sweet breads include banana bread, zucchini bread, and the Summer Zucchini Bread recipe you mentioned earlier.

Savory breads, on the other hand, rely more on umami flavors from ingredients like yeast, salt, and herbs to create a savory taste. They may also include spices, seeds, or nuts that add depth and complexity to their flavor profile. Examples of savory breads include cornbread, keto protein bread, and flatbreads.

While both types of bread can be delicious in their own right, the key difference lies in the balance of sweet and savory flavors.

Please enter your question or type 'exit' to exit: give me one sweet and one savoury bread recipie 
Assistant: Here are two bread recipes for you:

**Sweet Bread Recipe: Summer Zucchini Bread**

Ingredients:

* 1 cup granulated sugar
* 1/2 cup unsalted butter, softened
* 2 large eggs
* 2 cups grated zucchini
* 1 tsp vanilla extract
* 1 1/2 cups all-purpose flour
* 1 tsp baking powder
* 1/2 tsp salt
* 1/2 cup chopped walnuts (optional)

Instructions:

1. Preheat oven to 350°F (180°C). Grease a 9x5-inch loaf pan.
2. In a large bowl, whisk together sugar, butter, eggs, and vanilla extract.
3. Add zucchini and mix until well combined.
4. In a separate bowl, whisk together flour, baking powder, and salt.
5. Gradually add dry ingredients to wet ingredients and stir until just combined.
6. Fold in chopped walnuts (if using).
7. Pour batter into prepared loaf pan and bake for 55-60 minutes or until a toothpick comes out clean.

**Savory Bread Recipe: Flatbreads**

Ingredients:

* 1/2 cup sifted coconut flour
* 1/2 cup ground golden flaxseed
* 1 tsp baking soda
* 1/2 tsp sea salt
* 1 tsp tapioca flour
* 1/2 tsp cream of tartar
* 1 Tbsp + 1 tsp organic psyllium husk powder
* 1 cup warm water

Instructions:

1. Preheat oven to 400°F (200°C). Line a baking sheet with parchment paper.
2. In a large bowl, whisk together coconut flour, flaxseed, baking soda, sea salt, tapioca flour, and cream of tartar.
3. Gradually add psyllium husk powder and mix until well combined.
4. Add warm water and stir until dough forms.
5. Knead dough for 2-3 minutes until smooth and elastic.
6. Divide dough into 8-10 equal pieces.
7. Roll out each piece into a thin circle, about 1/8 inch thick.
8. Brush with olive oil and sprinkle with sesame seeds (if desired).
9. Bake for 12-15 minutes or until edges are golden brown.

Enjoy your delicious sweet and savory breads!

Please enter your question or type 'exit' to exit: exit
Goodbye
"""