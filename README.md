# oneShoppingList

## The one and only shopping list you need

### cs50: Final project by Kai R. Sehls

#### Video Demo: https://www.youtube.com/watch?v=E1SirArG2ik

## Description

### Disclaimer

I want to be a code monkey, not an ad writer or film producer. So please bear with me, if the required video demo and documentation is somewhat basic. Showmanship is none of my core skills and in any future job will be done by others rather than by me.

### Abstract

oneShoppingList will combine several different shopping lists – one for each kind of store – automatically display only the items available in a given store and in the order you will find them in said store.

### Idea

#### Problem

<!-- something something problems with shopping lists something -->
We all have at least once forgotten something when we went grocery shopping. In some cases that's more annoying than in others. That's why we use shopping lists.

But even with shopping lists every once in a while, when we finally reach the checkout counter, we notice that one last item on the list, that's located in the opposite corner of the store.

So we write our shopping list according to the positioning of the product categories inside the store. And as an exception and unplanned the next time we go shopping, it's in another store because it's conveniently sited on our way home from our field work that day. Of course in that store the positioning of the product categories is different to our usual store of choice. So our shopping list is in the wrong order, again.

What's more, this other store by chance has a much wider variety of products. Not only can you get your usual groceries here but also the light bulbs, batteries and storage cards, which, in order to buy them, you would have had to cumbersomely travel downtown to the big mall. But of course for that occasion you wrote a separate shopping list that you're not carrying with you here and now you cannot remember the exact specs you need.

#### Solution

What if you ever only needed to write one shopping list, no matter what kind of product you're planning or needing to buy? One shopping list for the grocery supermarket, the pet shop, the hardware store, the electronics discounter and even the bookseller's round the corner.

> Nay, that would be maddeningly confusing with all those different items on one single list! Or would it?

Don't worry, oneShoppingList has got you!

You just write down the stuff you need to buy in oneShoppingList. Yes, all of it. Yes, in the same one list. And you don't mind the order of the items either.

oneShoppingList does that for you, also.

In order to do so, you create a category-order-in-store list beforehand for the stores that you visit. Then oneShoppingList will sort your shopping list depending on the store that you're about to visit in the proper order. In doing so, oneShoppingList will not only take into account, which product categories there are in the store, but also the order of their positioning inside the store, so your list is always sorted correctly without beeing unnecessarily confusing, since it won't show items that aren't sold in that store anyway. (It will show them but separately and with a corresponding notice.)

## Setup and Usage

When first started, you will be redirected to the about page, where you will learn about the idea behind the app the usage and a little bit about me.

### Register

Your first step will be to register a user name and select a password. The password has no requirements except that it must contain at least one capital letter and at least one number.

If your user name is not in use by another user and your password meets the requirements you will be sent to the start page after registering. Of course there will be no shopping list yet. First the setup should be finished.

### Categories

Record all the categories that come to your mind when you envision going through all your favourite stores. This will create a list of categories in alphabetical order.

Categories can be changed but in order to not break any positioning or shopping lists only unused categories can be deleted.

### Items

In a future version of the app it will be possible to record new items »on the fly« while writing your shopping list on the start page but for now, all items that you want to put on the shopping list must be recorded here first.

Like categories, items can be changed and deleted, too. The latter again only as long as they are unused on any shopping list.

### Stores

Although it is not required to have any stores on record, it is highly recommended to enter some into the database, since it's the central feature of this app to display your shopping list according to the very store you're about to visit.

Keep in mind to choose unique store names when recording multiple branches of the same enterprise, or optionally add the corresponding adress of the store, to avoid confusion.

You can always alter and delete the store's record later.

#### Edit category order

Finally we're getting to the gist of the matter – the category positionings likely differing from store to store.

You'll find a _edit category order_ button next to each store listed on the stores page. Press it and the app will show the positioning order for the selected store. There you can choose from all the categories, that you've recorded previously, and add them to the categories available in this particular store.

Of course you also can rearrange the order if necessary and also add or delete categories in the store's positionings.

### Shopping list

You've set up everything now, so let's write your shopping list. Don't bother to think about the order of the items, just write everything that you need or want to buy.

Next time you visit a store, select that store on your start page and the order of the shopping list will magically be sorted according to the positioning in the store.

## Code

Of course I know, that inside many stores (at least where I live) there is no internet reception. So how does a shopping list programmed as a web application make any sense?

The surprisingly honest answer is, it doesn't. It makes no practical sense, that is. My final project probably will not be used afterwards in an actual shop. But obviously I had a reason for this decision.

I will port the app to Android and iOS via KIVY afterwards but I wanted to use the knowledge that Mr Malan and the cs50 team imparted to me throughout the course.

That's why I chose to realize this idea as a web app, using html, css, js, sql, python and flask. I tried to be as consistent with my usage of variable names but must admit that I sometimes could not resist to not take everything too serious, especially at the time I was coding in bed with fever from covid.

Also I as respectfully as gratefully somewhat copypasted the session code from cs50's finance problem set. I'm convinced if you had considered that code to be inferior you would not have us use it in the first place.

## Me

After having ludicrous fun with the Commodore VIC20, the C64 and the C128 throughout the 80s, learning and working as a radio- and television-technician in the 90s, for a few years I coded web applications for a living in the early 2000s – before they were even called web applications. As a self-taught entrepreneur I used html, css, sql and php to generate a humble but decent income.
Then fate struck twice. First merciful (2 children) then hard (severe illness). I had to realign not only my career but my whole life (to the better, in retrospect). I worked in retail and later as a truck driver until I now eventually got the chance again to become a programmer with this cs50 course. Thanks for this opportunity and please bear with me since english is not my native language.

I am Kai, this is my final project, these are my exam nerves and this was cs50.
