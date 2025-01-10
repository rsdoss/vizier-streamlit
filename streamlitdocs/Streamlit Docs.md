# Basic concepts of Streamlit

Working with Streamlit is simple. First you sprinkle a few Streamlit commands into a normal Python script, then you run it with `streamlit run`:

`streamlit run your_script.py [-- script args]`

As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab in your default web browser. The app is your canvas, where you'll draw charts, text, widgets, tables, and more.

What gets drawn in the app is up to you. For example [`st.text`](https://docs.streamlit.io/develop/api-reference/text/st.text) writes raw text to your app, and [`st.line_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart) draws — you guessed it — a line chart. Refer to our [API documentation](https://docs.streamlit.io/develop/api-reference) to see all commands that are available to you.

_push_pin_

#### Note

When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself.

Another way of running Streamlit is to run it as a Python module. This can be useful when configuring an IDE like PyCharm to work with Streamlit:

`# Running python -m streamlit run your_script.py # is equivalent to: streamlit run your_script.py`

_star_

#### Tip

You can also pass a URL to `streamlit run`! This is great when combined with GitHub Gists. For example:

`streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py`

## [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#development-flow)Development flow

Every time you want to update your app, save the source file. When you do that, Streamlit detects if there is a change and asks you whether you want to rerun your app. Choose "Always rerun" at the top-right of your screen to automatically update your app every time you change its source code.

This allows you to work in a fast interactive loop: you type some code, save it, try it out live, then type some more code, save it, try it out, and so on until you're happy with the results. This tight loop between coding and viewing results live is one of the ways Streamlit makes your life easier.

_star_

#### Tip

While developing a Streamlit app, it's recommended to lay out your editor and browser windows side by side, so the code and the app can be seen at the same time. Give it a try!

As of Streamlit version 1.10.0 and higher, Streamlit apps cannot be run from the root directory of Linux distributions. If you try to run a Streamlit app from the root directory, Streamlit will throw a `FileNotFoundError: [Errno 2] No such file or directory` error. For more information, see GitHub issue [#5239](https://github.com/streamlit/streamlit/issues/5239).

If you are using Streamlit version 1.10.0 or higher, your main script should live in a directory other than the root directory. When using Docker, you can use the `WORKDIR` command to specify the directory where your main script lives. For an example of how to do this, read [Create a Dockerfile](https://docs.streamlit.io/deploy/tutorials/docker#create-a-dockerfile).

## [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#data-flow)Data flow

Streamlit's architecture allows you to write apps the same way you write plain Python scripts. To unlock this, Streamlit apps have a unique data flow: any time something must be updated on the screen, Streamlit reruns your entire Python script from top to bottom.

This can happen in two situations:

- Whenever you modify your app's source code.
    
- Whenever a user interacts with widgets in the app. For example, when dragging a slider, entering text in an input box, or clicking a button.
    

Whenever a callback is passed to a widget via the `on_change` (or `on_click`) parameter, the callback will always run before the rest of your script. For details on the Callbacks API, please refer to our [Session State API Reference Guide](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state#use-callbacks-to-update-session-state).

And to make all of this fast and seamless, Streamlit does some heavy lifting for you behind the scenes. A big player in this story is the [`@st.cache_data`](https://docs.streamlit.io/get-started/fundamentals/main-concepts#caching) decorator, which allows developers to skip certain costly computations when their apps rerun. We'll cover caching later in this page.

## [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#display-and-style-data)Display and style data

There are a few ways to display data (tables, arrays, data frames) in Streamlit apps. [Below](https://docs.streamlit.io/get-started/fundamentals/main-concepts#use-magic), you will be introduced to _magic_ and [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write), which can be used to write anything from text to tables. After that, let's take a look at methods designed specifically for visualizing data.

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#use-magic)Use magic

You can also write to your app without calling any Streamlit methods. Streamlit supports "[magic commands](https://docs.streamlit.io/develop/api-reference/write-magic/magic)," which means you don't have to use [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write) at all! To see this in action try this snippet:

`""" # My first app Here's our first attempt at using data to create a table: """ import streamlit as st import pandas as pd df = pd.DataFrame({ 'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40] }) df`

Any time that Streamlit sees a variable or a literal value on its own line, it automatically writes that to your app using [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write). For more information, refer to the documentation on [magic commands](https://docs.streamlit.io/develop/api-reference/write-magic/magic).

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#write-a-data-frame)Write a data frame

Along with [magic commands](https://docs.streamlit.io/develop/api-reference/write-magic/magic), [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write) is Streamlit's "Swiss Army knife". You can pass almost anything to [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write): text, data, Matplotlib figures, Altair charts, and more. Don't worry, Streamlit will figure it out and render things the right way.

`import streamlit as st import pandas as pd st.write("Here's our first attempt at using data to create a table:") st.write(pd.DataFrame({ 'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40] }))`

There are other data specific functions like [`st.dataframe()`](https://docs.streamlit.io/develop/api-reference/data/st.dataframe) and [`st.table()`](https://docs.streamlit.io/develop/api-reference/data/st.table) that you can also use for displaying data. Let's understand when to use these features and how to add colors and styling to your data frames.

You might be asking yourself, "why wouldn't I always use `st.write()`?" There are a few reasons:

1. _Magic_ and [`st.write()`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write) inspect the type of data that you've passed in, and then decide how to best render it in the app. Sometimes you want to draw it another way. For example, instead of drawing a dataframe as an interactive table, you may want to draw it as a static table by using `st.table(df)`.
2. The second reason is that other methods return an object that can be used and modified, either by adding data to it or replacing it.
3. Finally, if you use a more specific Streamlit method you can pass additional arguments to customize its behavior.

For example, let's create a data frame and change its formatting with a Pandas `Styler` object. In this example, you'll use Numpy to generate a random sample, and the [`st.dataframe()`](https://docs.streamlit.io/develop/api-reference/data/st.dataframe) method to draw an interactive table.

_push_pin_

#### Note

This example uses Numpy to generate a random sample, but you can use Pandas DataFrames, Numpy arrays, or plain Python arrays.

`import streamlit as st import numpy as np dataframe = np.random.randn(10, 20) st.dataframe(dataframe)`

Let's expand on the first example using the Pandas `Styler` object to highlight some elements in the interactive table.

`import streamlit as st import numpy as np import pandas as pd dataframe = pd.DataFrame( np.random.randn(10, 20), columns=('col %d' % i for i in range(20))) st.dataframe(dataframe.style.highlight_max(axis=0))`

Streamlit also has a method for static table generation: [`st.table()`](https://docs.streamlit.io/develop/api-reference/data/st.table).

`import streamlit as st import numpy as np import pandas as pd dataframe = pd.DataFrame( np.random.randn(10, 20), columns=('col %d' % i for i in range(20))) st.table(dataframe)`

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#draw-charts-and-maps)Draw charts and maps

Streamlit supports several popular data charting libraries like [Matplotlib, Altair, deck.gl, and more](https://docs.streamlit.io/develop/api-reference#chart-elements). In this section, you'll add a bar chart, line chart, and a map to your app.

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#draw-a-line-chart)Draw a line chart

You can easily add a line chart to your app with [`st.line_chart()`](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart). We'll generate a random sample using Numpy and then chart it.

`import streamlit as st import numpy as np import pandas as pd chart_data = pd.DataFrame( np.random.randn(20, 3), columns=['a', 'b', 'c']) st.line_chart(chart_data)`

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#plot-a-map)Plot a map

With [`st.map()`](https://docs.streamlit.io/develop/api-reference/charts/st.map) you can display data points on a map. Let's use Numpy to generate some sample data and plot it on a map of San Francisco.

`import streamlit as st import numpy as np import pandas as pd map_data = pd.DataFrame( np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon']) st.map(map_data)`

## [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#widgets)Widgets

When you've got the data or model into the state that you want to explore, you can add in widgets like [`st.slider()`](https://docs.streamlit.io/develop/api-reference/widgets/st.slider), [`st.button()`](https://docs.streamlit.io/develop/api-reference/widgets/st.button) or [`st.selectbox()`](https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox). It's really straightforward — treat widgets as variables:

`import streamlit as st x = st.slider('x') # 👈 this is a widget st.write(x, 'squared is', x * x)`

On first run, the app above should output the text "0 squared is 0". Then every time a user interacts with a widget, Streamlit simply reruns your script from top to bottom, assigning the current state of the widget to your variable in the process.

For example, if the user moves the slider to position `10`, Streamlit will rerun the code above and set `x` to `10` accordingly. So now you should see the text "10 squared is 100".

Widgets can also be accessed by key, if you choose to specify a string to use as the unique key for the widget:

`import streamlit as st st.text_input("Your name", key="name") # You can access the value at any point with: st.session_state.name`

Every widget with a key is automatically added to Session State. For more information about Session State, its association with widget state, and its limitations, see [Session State API Reference Guide](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state).

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#use-checkboxes-to-showhide-data)Use checkboxes to show/hide data

One use case for checkboxes is to hide or show a specific chart or section in an app. [`st.checkbox()`](https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox) takes a single argument, which is the widget label. In this sample, the checkbox is used to toggle a conditional statement.

`import streamlit as st import numpy as np import pandas as pd if st.checkbox('Show dataframe'): chart_data = pd.DataFrame( np.random.randn(20, 3), columns=['a', 'b', 'c']) chart_data`

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#use-a-selectbox-for-options)Use a selectbox for options

Use [`st.selectbox`](https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox) to choose from a series. You can write in the options you want, or pass through an array or data frame column.

Let's use the `df` data frame we created earlier.

`import streamlit as st import pandas as pd df = pd.DataFrame({ 'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40] }) option = st.selectbox( 'Which number do you like best?', df['first column']) 'You selected: ', option`

## [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#layout)Layout

Streamlit makes it easy to organize your widgets in a left panel sidebar with [`st.sidebar`](https://docs.streamlit.io/develop/api-reference/layout/st.sidebar). Each element that's passed to [`st.sidebar`](https://docs.streamlit.io/develop/api-reference/layout/st.sidebar) is pinned to the left, allowing users to focus on the content in your app while still having access to UI controls.

For example, if you want to add a selectbox and a slider to a sidebar, use `st.sidebar.slider` and `st.sidebar.selectbox` instead of `st.slider` and `st.selectbox`:

`import streamlit as st # Add a selectbox to the sidebar: add_selectbox = st.sidebar.selectbox( 'How would you like to be contacted?', ('Email', 'Home phone', 'Mobile phone') ) # Add a slider to the sidebar: add_slider = st.sidebar.slider( 'Select a range of values', 0.0, 100.0, (25.0, 75.0) )`

Beyond the sidebar, Streamlit offers several other ways to control the layout of your app. [`st.columns`](https://docs.streamlit.io/develop/api-reference/layout/st.columns) lets you place widgets side-by-side, and [`st.expander`](https://docs.streamlit.io/develop/api-reference/layout/st.expander) lets you conserve space by hiding away large content.

`import streamlit as st left_column, right_column = st.columns(2) # You can use a column just like st.sidebar: left_column.button('Press me!') # Or even better, call Streamlit functions inside a "with" block: with right_column: chosen = st.radio( 'Sorting hat', ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")) st.write(f"You are in {chosen} house!")`

_push_pin_

#### Note

`st.echo` and `st.spinner` are not currently supported inside the sidebar or layout options. Rest assured, though, we're currently working on adding support for those too!

### [](https://docs.streamlit.io/get-started/fundamentals/main-concepts#show-progress)Show progress

When adding long running computations to an app, you can use [`st.progress()`](https://docs.streamlit.io/develop/api-reference/status/st.progress) to display status in real time.

First, let's import time. We're going to use the `time.sleep()` method to simulate a long running computation:

`import time`

Now, let's create a progress bar:

`import streamlit as st import time 'Starting a long computation...' # Add a placeholder latest_iteration = st.empty() bar = st.progress(0) for i in range(100): # Update the progress bar with each iteration. latest_iteration.text(f'Iteration {i+1}') bar.progress(i + 1) time.sleep(0.1) '...and now we\'re done!'`

# Advanced concepts of Streamlit

Now that you know how a Streamlit app runs and handles data, let's talk about being efficient. Caching allows you to save the output of a function so you can skip over it on rerun. Session State lets you save information for each user that is preserved between reruns. This not only allows you to avoid unecessary recalculation, but also allows you to create dynamic pages and handle progressive processes.

## [](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#caching)Caching

Caching allows your app to stay performant even when loading data from the web, manipulating large datasets, or performing expensive computations.

The basic idea behind caching is to store the results of expensive function calls and return the cached result when the same inputs occur again. This avoids repeated execution of a function with the same input values.

To cache a function in Streamlit, you need to apply a caching decorator to it. You have two choices:

- `st.cache_data` is the recommended way to cache computations that return data. Use `st.cache_data` when you use a function that returns a serializable data object (e.g. str, int, float, DataFrame, dict, list). **It creates a new copy of the data at each function call**, making it safe against [mutations and race conditions](https://docs.streamlit.io/develop/concepts/architecture/caching#mutation-and-concurrency-issues). The behavior of `st.cache_data` is what you want in most cases – so if you're unsure, start with `st.cache_data` and see if it works!
- `st.cache_resource` is the recommended way to cache global resources like ML models or database connections. Use `st.cache_resource` when your function returns unserializable objects that you don’t want to load multiple times. **It returns the cached object itself**, which is shared across all reruns and sessions without copying or duplication. If you mutate an object that is cached using `st.cache_resource`, that mutation will exist across all reruns and sessions.

Example:

`@st.cache_data def long_running_function(param1, param2): return …`

In the above example, `long_running_function` is decorated with `@st.cache_data`. As a result, Streamlit notes the following:

- The name of the function (`"long_running_function"`).
- The value of the inputs (`param1`, `param2`).
- The code within the function.

Before running the code within `long_running_function`, Streamlit checks its cache for a previously saved result. If it finds a cached result for the given function and input values, it will return that cached result and not rerun function's code. Otherwise, Streamlit executes the function, saves the result in its cache, and proceeds with the script run. During development, the cache updates automatically as the function code changes, ensuring that the latest changes are reflected in the cache.

![Streamlit's two caching decorators and their use cases. Use st.cache_data for anything you'd store in a database. Use st.cache_resource for anything you can't store in a database, like a connection to a database or a machine learning model.](https://docs.streamlit.io/images/caching-high-level-diagram.png)

Streamlit's two caching decorators and their use cases.

For more information about the Streamlit caching decorators, their configuration parameters, and their limitations, see [Caching](https://docs.streamlit.io/develop/concepts/architecture/caching).

## [](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#session-state)Session State

Session State provides a dictionary-like interface where you can save information that is preserved between script reruns. Use `st.session_state` with key or attribute notation to store and recall values. For example, `st.session_state["my_key"]` or `st.session_state.my_key`. Remember that widgets handle their statefulness all by themselves, so you won't always need to use Session State!

### [](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#what-is-a-session)What is a session?

A session is a single instance of viewing an app. If you view an app from two different tabs in your browser, each tab will have its own session. So each viewer of an app will have a Session State tied to their specific view. Streamlit maintains this session as the user interacts with the app. If the user refreshes their browser page or reloads the URL to the app, their Session State resets and they begin again with a new session.

### [](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#examples-of-using-session-state)Examples of using Session State

Here's a simple app that counts the number of times the page has been run. Every time you click the button, the script will rerun.

`import streamlit as st if "counter" not in st.session_state: st.session_state.counter = 0 st.session_state.counter += 1 st.header(f"This page has run {st.session_state.counter} times.") st.button("Run it again")`

- **First run:** The first time the app runs for each user, Session State is empty. Therefore, a key-value pair is created (`"counter":0`). As the script continues, the counter is immediately incremented (`"counter":1`) and the result is displayed: "This page has run 1 times." When the page has fully rendered, the script has finished and the Streamlit server waits for the user to do something. When that user clicks the button, a rerun begins.
    
- **Second run:** Since "counter" is already a key in Session State, it is not reinitialized. As the script continues, the counter is incremented (`"counter":2`) and the result is displayed: "This page has run 2 times."
    

There are a few common scenarios where Session State is helpful. As demonstrated above, Session State is used when you have a progressive process that you want to build upon from one rerun to the next. Session State can also be used to prevent recalculation, similar to caching. However, the differences are important:

- Caching associates stored values to specific functions and inputs. Cached values are accessible to all users across all sessions.
- Session State associates stored values to keys (strings). Values in session state are only available in the single session where it was saved.

If you have random number generation in your app, you'd likely use Session State. Here's an example where data is generated randomly at the beginning of each session. By saving this random information in Session State, each user gets different random data when they open the app but it won't keep changing on them as they interact with it. If you select different colors with the picker you'll see that the data does not get re-randomized with each rerun. (If you open the app in a new tab to start a new session, you'll see different data!)

`import streamlit as st import pandas as pd import numpy as np if "df" not in st.session_state: st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"]) st.header("Choose a datapoint color") color = st.color_picker("Color", "#FF0000") st.divider() st.scatter_chart(st.session_state.df, x="x", y="y", color=color)`

If you are pulling the same data for all users, you'd likely cache a function that retrieves that data. On the other hand, if you pull data specific to a user, such as querying their personal information, you may want to save that in Session State. That way, the queried data is only available in that one session.

As mentioned in [Basic concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts#widgets), Session State is also related to widgets. Widgets are magical and handle statefulness quietly on their own. As an advanced feature however, you can manipulate the value of widgets within your code by assigning keys to them. Any key assigned to a widget becomes a key in Session State tied to the value of the widget. This can be used to manipulate the widget. After you finish understanding the basics of Streamlit, check out our guide on [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior) to dig in the details if you're interested.

## [](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#connections)Connections

As hinted above, you can use `@st.cache_resource` to cache connections. This is the most general solution which allows you to use almost any connection from any Python library. However, Streamlit also offers a convenient way to handle some of the most popular connections, like SQL! `st.connection` takes care of the caching for you so you can enjoy fewer lines of code. Getting data from your database can be as easy as:

`import streamlit as st conn = st.connection("my_database") df = conn.query("select * from my_table") st.dataframe(df)`

Of course, you may be wondering where your username and password go. Streamlit has a convenient mechanism for [Secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management). For now, let's just see how `st.connection` works very nicely with secrets. In your local project directory, you can save a `.streamlit/secrets.toml` file. You save your secrets in the toml file and `st.connection` just uses them! For example, if you have an app file `streamlit_app.py` your project directory may look like this:

`your-LOCAL-repository/ ├── .streamlit/ │ └── secrets.toml # Make sure to gitignore this! └── streamlit_app.py`

For the above SQL example, your `secrets.toml` file might look like the following:

`[connections.my_database] type="sql" dialect="mysql" username="xxx" password="xxx" host="example.com" # IP or URL port=3306 # Port number database="mydb" # Database name`

Since you don't want to commit your `secrets.toml` file to your repository, you'll need to learn how your host handles secrets when you're ready to publish your app. Each host platform may have a different way for you to pass your secrets. If you use Streamlit Community Cloud for example, each deployed app has a settings menu where you can load your secrets. After you've written an app and are ready to deploy, you can read all about how to [Deploy your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app) on Community Cloud.

# Additional Streamlit features

So you've read all about Streamlit's [Basic concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) and gotten a taste of caching and Session State in [Advanced concepts](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts). But what about the bells and whistles? Here's a quick look at some extra features to take your app to the next level.

## [](https://docs.streamlit.io/get-started/fundamentals/additional-features#theming)Theming

Streamlit supports Light and Dark themes out of the box. Streamlit will first check if the user viewing an app has a Light or Dark mode preference set by their operating system and browser. If so, then that preference will be used. Otherwise, the Light theme is applied by default.

You can also change the active theme from "⋮" → "Settings".

![Changing Themes](https://docs.streamlit.io/images/change_theme.gif)

Want to add your own theme to an app? The "Settings" menu has a theme editor accessible by clicking on "Edit active theme". You can use this editor to try out different colors and see your app update live.

![Editing Themes](https://docs.streamlit.io/images/edit_theme.gif)

When you're happy with your work, themes can be saved by [setting config options](https://docs.streamlit.io/develop/concepts/configuration) in the `[theme]` config section. After you've defined a theme for your app, it will appear as "Custom Theme" in the theme selector and will be applied by default instead of the included Light and Dark themes.

More information about the options available when defining a theme can be found in the [theme option documentation](https://docs.streamlit.io/develop/concepts/configuration/theming).

_push_pin_

#### Note

The theme editor menu is available only in local development. If you've deployed your app using Streamlit Community Cloud, the "Edit active theme" button will no longer be displayed in the "Settings" menu.

_star_

#### Tip

Another way to experiment with different theme colors is to turn on the "Run on save" option, edit your config.toml file, and watch as your app reruns with the new theme colors applied.

## [](https://docs.streamlit.io/get-started/fundamentals/additional-features#pages)Pages

As apps grow large, it becomes useful to organize them into multiple pages. This makes the app easier to manage as a developer and easier to navigate as a user. Streamlit provides a frictionless way to create multipage apps.

We designed this feature so that building a multipage app is as easy as building a single-page app! Just add more pages to an existing app as follows:

1. In the folder containing your main script, create a new `pages` folder. Let’s say your main script is named `main_page.py`.
2. Add new `.py` files in the `pages` folder to add more pages to your app.
3. Run `streamlit run main_page.py` as usual.

That’s it! The `main_page.py` script will now correspond to the main page of your app. And you’ll see the other scripts from the `pages` folder in the sidebar page selector. The pages are listed according to filename (without file extensions and disregarding underscores). For example:

`main_page.py`

`import streamlit as st st.markdown("# Main page 🎈") st.sidebar.markdown("# Main page 🎈")`

`pages/page_2.py`

`import streamlit as st st.markdown("# Page 2 ❄️") st.sidebar.markdown("# Page 2 ❄️")`

`pages/page_3.py`

`import streamlit as st st.markdown("# Page 3 🎉") st.sidebar.markdown("# Page 3 🎉")`

  

Now run `streamlit run main_page.py` and view your shiny new multipage app!

![](https://docs.streamlit.io/images/mpa-main-concepts.gif)

Our documentation on [Multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps) teaches you how to add pages to your app, including how to define pages, structure and run multipage apps, and navigate between pages. Once you understand the basics, [create your first multipage app](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)!

## [](https://docs.streamlit.io/get-started/fundamentals/additional-features#custom-components)Custom components

If you can't find the right component within the Streamlit library, try out custom components to extend Streamlit's built-in functionality. Explore and browse through popular, community-created components in the [Components gallery](https://streamlit.io/components). If you dabble in frontend development, you can build your own custom component with Streamlit's [components API](https://docs.streamlit.io/develop/concepts/custom-components/intro).

## [](https://docs.streamlit.io/get-started/fundamentals/additional-features#static-file-serving)Static file serving

As you learned in Streamlit fundamentals, Streamlit runs a server that clients connect to. That means viewers of your app don't have direct access to the files which are local to your app. Most of the time, this doesn't matter because Streamlt commands handle that for you. When you use `st.image(<path-to-image>)` your Streamlit server will access the file and handle the necessary hosting so your app viewers can see it. However, if you want a direct URL to an image or file you'll need to host it. This requires setting the correct configuration and placing your hosted files in a directory named `static`. For example, your project could look like:

`your-project/ ├── static/ │ └── my_hosted-image.png └── streamlit_app.py`

To learn more, read our guide on [Static file serving](https://docs.streamlit.io/develop/concepts/configuration/serving-static-files).

## [](https://docs.streamlit.io/get-started/fundamentals/additional-features#app-testing)App testing

Good development hygiene includes testing your code. Automated testing allows you to write higher quality code, faster! Streamlit has a built-in testing framework that let's you build tests easily. Use your favorite testing framework to run your tests. We like [`pytest`](https://pypi.org/project/pytest/). When you test a Streamlit app, you simulate running the app, declare user input, and inspect the results. You can use GitHub workflows to automate your tests and get instant alerts about breaking changes. Learn more in our guide to [App testing](https://docs.streamlit.io/develop/concepts/app-testing).

# App model summary

Now that you know a little more about all the individual pieces, let's close the loop and review how it works together:

1. Streamlit apps are Python scripts that run from top to bottom.
2. Every time a user opens a browser tab pointing to your app, the script is executed and a new session starts.
3. As the script executes, Streamlit draws its output live in a browser.
4. Every time a user interacts with a widget, your script is re-executed and Streamlit redraws its output in the browser.
    - The output value of that widget matches the new value during that rerun.
5. Scripts use the Streamlit cache to avoid recomputing expensive functions, so updates happen very fast.
6. Session State lets you save information that persists between reruns when you need more than a simple widget.
7. Streamlit apps can contain multiple pages, which are defined in separate `.py` files in a `pages` folder.

![The Streamlit app model](https://docs.streamlit.io/images/app_model.png)

# Create an app

If you've made it this far, chances are you've [installed Streamlit](https://docs.streamlit.io/get-started/installation) and run through the basics in [Basic concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) and [Advanced concepts](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts). If not, now is a good time to take a look.

The easiest way to learn how to use Streamlit is to try things out yourself. As you read through this guide, test each method. As long as your app is running, every time you add a new element to your script and save, Streamlit's UI will ask if you'd like to rerun the app and view the changes. This allows you to work in a fast interactive loop: you write some code, save it, review the output, write some more, and so on, until you're happy with the results. The goal is to use Streamlit to create an interactive app for your data or model and along the way to use Streamlit to review, debug, perfect, and share your code.

In this guide, you're going to use Streamlit's core features to create an interactive app; exploring a public Uber dataset for pickups and drop-offs in New York City. When you're finished, you'll know how to fetch and cache data, draw charts, plot information on a map, and use interactive widgets, like a slider, to filter results.

_star_

#### Tip

If you'd like to skip ahead and see everything at once, the [complete script is available below](https://docs.streamlit.io/get-started/tutorials/create-an-app#lets-put-it-all-together).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#create-your-first-app)Create your first app

Streamlit is more than just a way to make data apps, it’s also a community of creators that share their apps and ideas and help each other make their work better. Please come join us on the community forum. We love to hear your questions, ideas, and help you work through your bugs — stop by today!

1. The first step is to create a new Python script. Let's call it `uber_pickups.py`.
    
2. Open `uber_pickups.py` in your favorite IDE or text editor, then add these lines:
    
    `import streamlit as st import pandas as pd import numpy as np`
    
3. Every good app has a title, so let's add one:
    
    `st.title('Uber pickups in NYC')`
    
4. Now it's time to run Streamlit from the command line:
    
    `streamlit run uber_pickups.py`
    
    Running a Streamlit app is no different than any other Python script. Whenever you need to view the app, you can use this command.
    
    _star_
    
    #### Tip
    
    Did you know you can also pass a URL to `streamlit run`? This is great when combined with GitHub Gists. For example:
    
    `streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py`
    
5. As usual, the app should automatically open in a new tab in your browser.
    

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#fetch-some-data)Fetch some data

Now that you have an app, the next thing you'll need to do is fetch the Uber dataset for pickups and drop-offs in New York City.

1. Let's start by writing a function to load the data. Add this code to your script:
    
    `DATE_COLUMN = 'date/time' DATA_URL = ('https://s3-us-west-2.amazonaws.com/' 'streamlit-demo-data/uber-raw-data-sep14.csv.gz') def load_data(nrows): data = pd.read_csv(DATA_URL, nrows=nrows) lowercase = lambda x: str(x).lower() data.rename(lowercase, axis='columns', inplace=True) data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) return data`
    
    You'll notice that `load_data` is a plain old function that downloads some data, puts it in a Pandas dataframe, and converts the date column from text to datetime. The function accepts a single parameter (`nrows`), which specifies the number of rows that you want to load into the dataframe.
    
2. Now let's test the function and review the output. Below your function, add these lines:
    
    `# Create a text element and let the reader know the data is loading. data_load_state = st.text('Loading data...') # Load 10,000 rows of data into the dataframe. data = load_data(10000) # Notify the reader that the data was successfully loaded. data_load_state.text('Loading data...done!')`
    
    You'll see a few buttons in the upper-right corner of your app asking if you'd like to rerun the app. Choose **Always rerun**, and you'll see your changes automatically each time you save.
    

Ok, that's underwhelming...

It turns out that it takes a long time to download data, and load 10,000 lines into a dataframe. Converting the date column into datetime isn’t a quick job either. You don’t want to reload the data each time the app is updated – luckily Streamlit allows you to cache the data.

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#effortless-caching)Effortless caching

1. Try adding `@st.cache_data` before the `load_data` declaration:
    
    `@st.cache_data def load_data(nrows):`
    
2. Then save the script, and Streamlit will automatically rerun your app. Since this is the first time you’re running the script with `@st.cache_data`, you won't see anything change. Let’s tweak your file a little bit more so that you can see the power of caching.
    
3. Replace the line `data_load_state.text('Loading data...done!')` with this:
    
    `data_load_state.text("Done! (using st.cache_data)")`
    
4. Now save. See how the line you added appeared immediately? If you take a step back for a second, this is actually quite amazing. Something magical is happening behind the scenes, and it only takes one line of code to activate it.
    

### [](https://docs.streamlit.io/get-started/tutorials/create-an-app#hows-it-work)How's it work?

Let's take a few minutes to discuss how `@st.cache_data` actually works.

When you mark a function with Streamlit’s cache annotation, it tells Streamlit that whenever the function is called that it should check two things:

1. The input parameters you used for the function call.
2. The code inside the function.

If this is the first time Streamlit has seen both these items, with these exact values, and in this exact combination, it runs the function and stores the result in a local cache. The next time the function is called, if the two values haven't changed, then Streamlit knows it can skip executing the function altogether. Instead, it reads the output from the local cache and passes it on to the caller -- like magic.

"But, wait a second," you’re saying to yourself, "this sounds too good to be true. What are the limitations of all this awesomesauce?"

Well, there are a few:

1. Streamlit will only check for changes within the current working directory. If you upgrade a Python library, Streamlit's cache will only notice this if that library is installed inside your working directory.
2. If your function is not deterministic (that is, its output depends on random numbers), or if it pulls data from an external time-varying source (for example, a live stock market ticker service) the cached value will be none-the-wiser.
3. Lastly, you should avoid mutating the output of a function cached with `st.cache_data` since cached values are stored by reference.

While these limitations are important to keep in mind, they tend not to be an issue a surprising amount of the time. Those times, this cache is really transformational.

_star_

#### Tip

Whenever you have a long-running computation in your code, consider refactoring it so you can use `@st.cache_data`, if possible. Please read [Caching](https://docs.streamlit.io/develop/concepts/architecture/caching) for more details.

Now that you know how caching with Streamlit works, let’s get back to the Uber pickup data.

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#inspect-the-raw-data)Inspect the raw data

It's always a good idea to take a look at the raw data you're working with before you start working with it. Let's add a subheader and a printout of the raw data to the app:

`st.subheader('Raw data') st.write(data)`

In the [Basic concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) guide you learned that [`st.write`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write) will render almost anything you pass to it. In this case, you're passing in a dataframe and it's rendering as an interactive table.

[`st.write`](https://docs.streamlit.io/develop/api-reference/write-magic/st.write) tries to do the right thing based on the data type of the input. If it isn't doing what you expect you can use a specialized command like [`st.dataframe`](https://docs.streamlit.io/develop/api-reference/data/st.dataframe) instead. For a full list, see [API reference](https://docs.streamlit.io/develop/api-reference).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#draw-a-histogram)Draw a histogram

Now that you've had a chance to take a look at the dataset and observe what's available, let's take things a step further and draw a histogram to see what Uber's busiest hours are in New York City.

1. To start, let's add a subheader just below the raw data section:
    
    `st.subheader('Number of pickups by hour')`
    
2. Use NumPy to generate a histogram that breaks down pickup times binned by hour:
    
    `hist_values = np.histogram( data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]`
    
3. Now, let's use Streamlit's [`st.bar_chart()`](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart) method to draw this histogram.
    
    `st.bar_chart(hist_values)`
    
4. Save your script. This histogram should show up in your app right away. After a quick review, it looks like the busiest time is 17:00 (5 P.M.).
    

To draw this diagram we used Streamlit's native `bar_chart()` method, but it's important to know that Streamlit supports more complex charting libraries like Altair, Bokeh, Plotly, Matplotlib and more. For a full list, see [supported charting libraries](https://docs.streamlit.io/develop/api-reference/charts).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#plot-data-on-a-map)Plot data on a map

Using a histogram with Uber's dataset helped us determine what the busiest times are for pickups, but what if we wanted to figure out where pickups were concentrated throughout the city. While you could use a bar chart to show this data, it wouldn't be easy to interpret unless you were intimately familiar with latitudinal and longitudinal coordinates in the city. To show pickup concentration, let's use Streamlit [`st.map()`](https://docs.streamlit.io/develop/api-reference/charts/st.map) function to overlay the data on a map of New York City.

1. Add a subheader for the section:
    
    `st.subheader('Map of all pickups')`
    
2. Use the `st.map()` function to plot the data:
    
    `st.map(data)`
    
3. Save your script. The map is fully interactive. Give it a try by panning or zooming in a bit.
    

After drawing your histogram, you determined that the busiest hour for Uber pickups was 17:00. Let's redraw the map to show the concentration of pickups at 17:00.

1. Locate the following code snippet:
    
    `st.subheader('Map of all pickups') st.map(data)`
    
2. Replace it with:
    
    `hour_to_filter = 17 filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] st.subheader(f'Map of all pickups at {hour_to_filter}:00') st.map(filtered_data)`
    
3. You should see the data update instantly.
    

To draw this map we used the [`st.map`](https://docs.streamlit.io/develop/api-reference/charts/st.map) function that's built into Streamlit, but if you'd like to visualize complex map data, we encourage you to take a look at the [`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#filter-results-with-a-slider)Filter results with a slider

In the last section, when you drew the map, the time used to filter results was hardcoded into the script, but what if we wanted to let a reader dynamically filter the data in real time? Using Streamlit's widgets you can. Let's add a slider to the app with the `st.slider()` method.

1. Locate `hour_to_filter` and replace it with this code snippet:
    
    `hour_to_filter = st.slider('hour', 0, 23, 17) # min: 0h, max: 23h, default: 17h`
    
2. Use the slider and watch the map update in real time.
    

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#use-a-button-to-toggle-data)Use a button to toggle data

Sliders are just one way to dynamically change the composition of your app. Let's use the [`st.checkbox`](https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox) function to add a checkbox to your app. We'll use this checkbox to show/hide the raw data table at the top of your app.

1. Locate these lines:
    
    `st.subheader('Raw data') st.write(data)`
    
2. Replace these lines with the following code:
    
    `if st.checkbox('Show raw data'): st.subheader('Raw data') st.write(data)`
    

We're sure you've got your own ideas. When you're done with this tutorial, check out all the widgets that Streamlit exposes in our [API Reference](https://docs.streamlit.io/develop/api-reference).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#lets-put-it-all-together)Let's put it all together

That's it, you've made it to the end. Here's the complete script for our interactive app.

_star_

#### Tip

If you've skipped ahead, after you've created your script, the command to run Streamlit is `streamlit run [app name]`.

`import streamlit as st import pandas as pd import numpy as np st.title('Uber pickups in NYC') DATE_COLUMN = 'date/time' DATA_URL = ('https://s3-us-west-2.amazonaws.com/' 'streamlit-demo-data/uber-raw-data-sep14.csv.gz') @st.cache_data def load_data(nrows): data = pd.read_csv(DATA_URL, nrows=nrows) lowercase = lambda x: str(x).lower() data.rename(lowercase, axis='columns', inplace=True) data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) return data data_load_state = st.text('Loading data...') data = load_data(10000) data_load_state.text("Done! (using st.cache_data)") if st.checkbox('Show raw data'): st.subheader('Raw data') st.write(data) st.subheader('Number of pickups by hour') hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] st.bar_chart(hist_values) # Some number in the range 0-23 hour_to_filter = st.slider('hour', 0, 23, 17) filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] st.subheader('Map of all pickups at %s:00' % hour_to_filter) st.map(filtered_data)`

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#share-your-app)Share your app

After you’ve built a Streamlit app, it's time to share it! To show it off to the world you can use **Streamlit Community Cloud** to deploy, manage, and share your app for free.

It works in 3 simple steps:

1. Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
2. Sign into [share.streamlit.io](https://share.streamlit.io/)
3. Click 'Deploy an app' and then paste in your GitHub URL

That's it! 🎈 You now have a publicly deployed app that you can share with the world. Click to learn more about [how to use Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).

## [](https://docs.streamlit.io/get-started/tutorials/create-an-app#get-help)Get help

That's it for getting started, now you can go and build your own apps! If you run into difficulties here are a few things you can do.

- Check out our [community forum](https://discuss.streamlit.io/) and post a question
- Quick help from command line with `streamlit help`
- Go through our [Knowledge Base](https://docs.streamlit.io/knowledge-base) for tips, step-by-step tutorials, and articles that answer your questions about creating and deploying Streamlit apps.
- Read more documentation! Check out:
    - [Concepts](https://docs.streamlit.io/develop/concepts) for things like caching, theming, and adding statefulness to apps.
    - [API reference](https://docs.streamlit.io/develop/api-reference/) for examples of every Streamlit command.
-

# Create a multipage app

In [Additional features](https://docs.streamlit.io/get-started/fundamentals/additional-features), we introduced multipage apps, including how to define pages, structure and run multipage apps, and navigate between pages in the user interface. You can read more details in our guide to [Multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps)

In this guide, let’s put our understanding of multipage apps to use by converting the previous version of our `streamlit hello` app to a multipage app!

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#motivation)Motivation

Before Streamlit 1.10.0, the streamlit hello command was a large single-page app. As there was no support for multiple pages, we resorted to splitting the app's content using `st.selectbox` in the sidebar to choose what content to run. The content is comprised of three demos for plotting, mapping, and dataframes.

Here's what the code and single-page app looked like:

**`hello.py`** (👈 Toggle to expand)  

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-hello.streamlit.app/?utm_medium=oembed)

Notice how large the file is! Each app “page" is written as a function, and the selectbox is used to pick which page to display. As our app grows, maintaining the code requires a lot of additional overhead. Moreover, we’re limited by the `st.selectbox` UI to choose which “page" to run, we cannot customize individual page titles with `st.set_page_config`, and we’re unable to navigate between pages using URLs.

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#convert-an-existing-app-into-a-multipage-app)Convert an existing app into a multipage app

Now that we've identified the limitations of a single-page app, what can we do about it? Armed with our knowledge from the previous section, we can convert the existing app to be a multipage app, of course! At a high level, we need to perform the following steps:

1. Create a new `pages` folder in the same folder where the “entrypoint file" (`hello.py`) lives
2. Rename our entrypoint file to `Hello.py` , so that the title in the sidebar is capitalized
3. Create three new files inside of `pages`:
    - `pages/1_📈_Plotting_Demo.py`
    - `pages/2_🌍_Mapping_Demo.py`
    - `pages/3_📊_DataFrame_Demo.py`
4. Move the contents of the `plotting_demo`, `mapping_demo`, and `data_frame_demo` functions into their corresponding new files from Step 3
5. Run `streamlit run Hello.py` to view your newly converted multipage app!

Now, let’s walk through each step of the process and view the corresponding changes in code.

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#create-the-entrypoint-file)Create the entrypoint file

`Hello.py`

`import streamlit as st st.set_page_config( page_title="Hello", page_icon="👋", ) st.write("# Welcome to Streamlit! 👋") st.sidebar.success("Select a demo above.") st.markdown( """ Streamlit is an open-source app framework built specifically for Machine Learning and Data Science projects. **👈 Select a demo from the sidebar** to see some examples of what Streamlit can do! ### Want to learn more? - Check out [streamlit.io](https://streamlit.io) - Jump into our [documentation](https://docs.streamlit.io) - Ask a question in our [community forums](https://discuss.streamlit.io) ### See more complex demos - Use a neural net to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving) - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups) """ )`

  

We rename our entrypoint file to `Hello.py` , so that the title in the sidebar is capitalized and only the code for the intro page is included. Additionally, we’re able to customize the page title and favicon — as it appears in the browser tab with `st.set_page_config`. We can do so for each of our pages too!

![](https://docs.streamlit.io/images/mpa-hello.png)

Notice how the sidebar does not contain page labels as we haven’t created any pages yet.

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#create-multiple-pages)Create multiple pages

A few things to remember here:

1. We can change the ordering of pages in our MPA by adding numbers to the beginning of each Python file. If we add a 1 to the front of our file name, Streamlit will put that file first in the list.
2. The name of each Streamlit app is determined by the file name, so to change the app name you need to change the file name!
3. We can add some fun to our app by adding emojis to our file names that will render in our Streamlit app.
4. Each page will have its own URL, defined by the name of the file.

Check out how we do all this below! For each new page, we create a new file inside the pages folder, and add the appropriate demo code into it.

  
`pages/1_📈_Plotting_Demo.py`

![](https://docs.streamlit.io/images/mpa-plotting-demo.png)

`pages/2_🌍_Mapping_Demo.py`

![](https://docs.streamlit.io/images/mpa-mapping-demo.png)

`pages/3_📊_DataFrame_Demo.py`

![](https://docs.streamlit.io/images/mpa-dataframe-demo.png)

With our additional pages created, we can now put it all together in the final step below.

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#run-the-multipage-app)Run the multipage app

To run your newly converted multipage app, run:

`streamlit run Hello.py`

That’s it! The `Hello.py` script now corresponds to the main page of your app, and other scripts that Streamlit finds in the pages folder will also be present in the new page selector that appears in the sidebar.

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-mpa-hello.streamlit.app/?utm_medium=oembed)

## [](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app#next-steps)Next steps

Congratulations! 🎉 If you've read this far, chances are you've learned to create both single-page and multipage apps. Where you go from here is entirely up to your creativity! We’re excited to see what you’ll build now that adding additional pages to your apps is easier than ever. Try adding more pages to the app we've just built as an exercise. Also, stop by the forum to show off your multipage apps with the Streamlit community! 🎈

Here are a few resources to help you get started:

- Deploy your app for free on Streamlit's [Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).
- Post a question or share your multipage app on our [community forum](https://discuss.streamlit.io/c/streamlit-examples/9).
- Check out our documentation on [Multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps).
- Read through [Concepts](https://docs.streamlit.io/develop/concepts) for things like caching, theming, and adding statefulness to apps.
- Browse our [API reference](https://docs.streamlit.io/develop/api-reference/) for examples of every Streamlit command.

# Streamlit API cheat sheet

This is a summary of the docs for the latest version of Streamlit, [v1.41.0](https://pypi.org/project/streamlit/1.41.0/).

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#install--import)Install & Import

`pip install streamlit streamlit run first_app.py # Import convention >>> import streamlit as st`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#pre-release-features)Pre-release features

`pip uninstall streamlit pip install streamlit-nightly --upgrade`

Learn more about [experimental features](https://docs.streamlit.io/develop/quick-reference/advanced-features/prerelease#experimental-features)

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#command-line)Command line

`streamlit --help streamlit run your_script.py streamlit hello streamlit config show streamlit cache clear streamlit docs streamlit --version`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#magic-commands)Magic commands

`# Magic commands implicitly # call st.write(). "_This_ is some **Markdown**" my_variable "dataframe:", my_data_frame`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-text)Display text

`st.write("Most objects") # df, err, func, keras! st.write(["st", "is <", 3]) st.write_stream(my_generator) st.write_stream(my_llm_stream) st.text("Fixed width text") st.markdown("_Markdown_") st.latex(r""" e^{i\pi} + 1 = 0 """) st.title("My title") st.header("My header") st.subheader("My sub") st.code("for i in range(8): foo()") st.html("<p>Hi!</p>")`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-data)Display data

`st.dataframe(my_dataframe) st.table(data.iloc[0:10]) st.json({"foo":"bar","fu":"ba"}) st.metric("My metric", 42, 2)`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-media)Display media

`st.image("./header.png") st.audio(data) st.video(data) st.video(data, subtitles="./subs.vtt") st.logo("logo.jpg")`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-charts)Display charts

`st.area_chart(df) st.bar_chart(df) st.bar_chart(df, horizontal=True) st.line_chart(df) st.map(df) st.scatter_chart(df) st.altair_chart(chart) st.bokeh_chart(fig) st.graphviz_chart(fig) st.plotly_chart(fig) st.pydeck_chart(chart) st.pyplot(fig) st.vega_lite_chart(df, spec) # Work with user selections event = st.plotly_chart( df, on_select="rerun" ) event = st.altair_chart( chart, on_select="rerun" ) event = st.vega_lite_chart( df, spec, on_select="rerun" )`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#add-elements-to-sidebar)Add elements to sidebar

`# Just add it after st.sidebar: a = st.sidebar.radio("Select one:", [1, 2]) # Or use "with" notation: with st.sidebar: st.radio("Select one:", [1, 2])`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#columns)Columns

`# Two equal columns: col1, col2 = st.columns(2) col1.write("This is column 1") col2.write("This is column 2") # Three different columns: col1, col2, col3 = st.columns([3, 1, 1]) # col1 is larger. # Bottom-aligned columns col1, col2 = st.columns(2, vertical_alignment="bottom") # You can also use "with" notation: with col1: st.radio("Select one:", [1, 2])`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#tabs)Tabs

`# Insert containers separated into tabs: tab1, tab2 = st.tabs(["Tab 1", "Tab2"]) tab1.write("this is tab 1") tab2.write("this is tab 2") # You can also use "with" notation: with tab1: st.radio("Select one:", [1, 2])`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#expandable-containers)Expandable containers

`expand = st.expander("My label", icon=":material/info:") expand.write("Inside the expander.") pop = st.popover("Button label") pop.checkbox("Show all") # You can also use "with" notation: with expand: st.radio("Select one:", [1, 2])`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#control-flow)Control flow

`# Stop execution immediately: st.stop() # Rerun script immediately: st.rerun() # Navigate to another page: st.switch_page("pages/my_page.py") # Define a navigation widget in your entrypoint file pg = st.navigation( st.Page("page1.py", title="Home", url_path="home", default=True) st.Page("page2.py", title="Preferences", url_path="settings") ) pg.run() # Group multiple widgets: with st.form(key="my_form"): username = st.text_input("Username") password = st.text_input("Password") st.form_submit_button("Login") # Define a dialog function @st.dialog("Welcome!") def modal_dialog(): st.write("Hello") modal_dialog() # Define a fragment @st.fragment def fragment_function(): df = get_data() st.line_chart(df) st.button("Update") fragment_function()`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-interactive-widgets)Display interactive widgets

`st.button("Click me") st.download_button("Download file", data) st.link_button("Go to gallery", url) st.page_link("app.py", label="Home") st.data_editor("Edit data", data) st.checkbox("I agree") st.feedback("thumbs") st.pills("Tags", ["Sports", "Politics"]) st.radio("Pick one", ["cats", "dogs"]) st.segmented_control("Filter", ["Open", "Closed"]) st.toggle("Enable") st.selectbox("Pick one", ["cats", "dogs"]) st.multiselect("Buy", ["milk", "apples", "potatoes"]) st.slider("Pick a number", 0, 100) st.select_slider("Pick a size", ["S", "M", "L"]) st.text_input("First name") st.number_input("Pick a number", 0, 10) st.text_area("Text to translate") st.date_input("Your birthday") st.time_input("Meeting time") st.file_uploader("Upload a CSV") st.audio_input("Record a voice message") st.camera_input("Take a picture") st.color_picker("Pick a color") # Use widgets' returned values in variables: for i in range(int(st.number_input("Num:"))): foo() if st.sidebar.selectbox("I:",["f"]) == "f": b() my_slider_val = st.slider("Quinn Mallory", 1, 88) st.write(slider_val) # Disable widgets to remove interactivity: st.slider("Pick a number", 0, 100, disabled=True)`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#build-chat-based-apps)Build chat-based apps

`# Insert a chat message container. with st.chat_message("user"): st.write("Hello 👋") st.line_chart(np.random.randn(30, 3)) # Display a chat input widget at the bottom of the app. >>> st.chat_input("Say something") # Display a chat input widget inline. with st.container(): st.chat_input("Say something")`

Learn how to [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#mutate-data)Mutate data

`# Add rows to a dataframe after # showing it. element = st.dataframe(df1) element.add_rows(df2) # Add rows to a chart after # showing it. element = st.line_chart(df1) element.add_rows(df2)`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-code)Display code

`with st.echo(): st.write("Code will be executed and printed")`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#placeholders-help-and-options)Placeholders, help, and options

`# Replace any single element. element = st.empty() element.line_chart(...) element.text_input(...) # Replaces previous. # Insert out of order. elements = st.container() elements.line_chart(...) st.write("Hello") elements.text_input(...) # Appears above "Hello". st.help(pandas.DataFrame) st.get_option(key) st.set_option(key, value) st.set_page_config(layout="wide") st.query_params[key] st.query_params.from_dict(params_dict) st.query_params.get_all(key) st.query_params.clear() st.html("<p>Hi!</p>")`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#connect-to-data-sources)Connect to data sources

`st.connection("pets_db", type="sql") conn = st.connection("sql") conn = st.connection("snowflake") class MyConnection(BaseConnection[myconn.MyConnection]): def _connect(self, **kwargs) -> MyConnection: return myconn.connect(**self._secrets, **kwargs) def query(self, query): return self._instance.query(query)`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#optimize-performance)Optimize performance

###### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#cache-data-objects)Cache data objects

`# E.g. Dataframe computation, storing downloaded data, etc. @st.cache_data def foo(bar): # Do something expensive and return data return data # Executes foo d1 = foo(ref1) # Does not execute foo # Returns cached item by value, d1 == d2 d2 = foo(ref1) # Different arg, so function foo executes d3 = foo(ref2) # Clear the cached value for foo(ref1) foo.clear(ref1) # Clear all cached entries for this function foo.clear() # Clear values from *all* in-memory or on-disk cached functions st.cache_data.clear()`

###### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#cache-global-resources)Cache global resources

`# E.g. TensorFlow session, database connection, etc. @st.cache_resource def foo(bar): # Create and return a non-data object return session # Executes foo s1 = foo(ref1) # Does not execute foo # Returns cached item by reference, s1 == s2 s2 = foo(ref1) # Different arg, so function foo executes s3 = foo(ref2) # Clear the cached value for foo(ref1) foo.clear(ref1) # Clear all cached entries for this function foo.clear() # Clear all global resources from cache st.cache_resource.clear()`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-progress-and-status)Display progress and status

`# Show a spinner during a process with st.spinner(text="In progress"): time.sleep(3) st.success("Done") # Show and update progress bar bar = st.progress(50) time.sleep(3) bar.progress(100) with st.status("Authenticating...") as s: time.sleep(2) st.write("Some long response.") s.update(label="Response") st.balloons() st.snow() st.toast("Warming up...") st.error("Error message") st.warning("Warning message") st.info("Info message") st.success("Success message") st.exception(e)`

#### [](https://docs.streamlit.io/develop/quick-reference/cheat-sheet#personalize-apps-for-users)Personalize apps for users

`# Show different content based on the user's email address. if st.experimental_user.email == "jane@examples.com": display_jane_content() elif st.experimental_user.email == "adam@example.com": display_adam_content() else: st.write("Please contact us to get access!") # Get dictionaries of cookies and headers st.context.cookies st.context.headers`

# Build a basic LLM chat app

## [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#introduction)Introduction

The advent of large language models like GPT has revolutionized the ease of developing chat-based applications. Streamlit offers several [Chat elements](https://docs.streamlit.io/develop/api-reference/chat), enabling you to build Graphical User Interfaces (GUIs) for conversational agents or chatbots. Leveraging [session state](https://docs.streamlit.io/develop/concepts/architecture/session-state) along with these elements allows you to construct anything from a basic chatbot to a more advanced, ChatGPT-like experience using purely Python code.

In this tutorial, we'll start by walking through Streamlit's chat elements, `st.chat_message` and `st.chat_input`. Then we'll proceed to construct three distinct applications, each showcasing an increasing level of complexity and functionality:

1. First, we'll [Build a bot that mirrors your input](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-bot-that-mirrors-your-input) to get a feel for the chat elements and how they work. We'll also introduce [session state](https://docs.streamlit.io/develop/concepts/architecture/session-state) and how it can be used to store the chat history. This section will serve as a foundation for the rest of the tutorial.
2. Next, you'll learn how to [Build a simple chatbot GUI with streaming](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming).
3. Finally, we'll [Build a ChatGPT-like app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app) that leverages session state to remember conversational context, all within less than 50 lines of code.

Here's a sneak peek of the LLM-powered chatbot GUI with streaming we'll build in this tutorial:

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-llm.streamlit.app/?utm_medium=oembed)

Play around with the above demo to get a feel for what we'll build in this tutorial. A few things to note:

- There's a chat input at the bottom of the screen that's always visible. It contains some placeholder text. You can type in a message and press Enter or click the run button to send it.
- When you enter a message, it appears as a chat message in the container above. The container is scrollable, so you can scroll up to see previous messages. A default avatar is displayed to your messages' left.
- The assistant's responses are streamed to the frontend and are displayed with a different default avatar.

Before we start building, let's take a closer look at the chat elements we'll use.

## [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#chat-elements)Chat elements

Streamlit offers several commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.

[`st.chat_message`](https://docs.streamlit.io/develop/api-reference/chat/st.chat_message) lets you insert a chat message container into the app so you can display messages from the user or the app. Chat containers can contain other Streamlit elements, including charts, tables, text, and more. [`st.chat_input`](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input) lets you display a chat input widget so the user can type in a message.

For an overview of the API, check out this video tutorial by Chanin Nantasenamat ([@dataprofessor](https://www.youtube.com/dataprofessor)), a Senior Developer Advocate at Streamlit.

### [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#stchat_message)st.chat_message

`st.chat_message` lets you insert a multi-element chat message container into your app. The returned container can contain any Streamlit element, including charts, tables, text, and more. To add elements to the returned container, you can use `with` notation.

`st.chat_message`'s first parameter is the `name` of the message author, which can be either `"user"` or `"assistant"` to enable preset styling and avatars, like in the demo above. You can also pass in a custom string to use as the author name. Currently, the name is not shown in the UI but is only set as an accessibility label. For accessibility reasons, you should not use an empty string.

Here's an minimal example of how to use `st.chat_message` to display a welcome message:

`import streamlit as st with st.chat_message("user"): st.write("Hello 👋")`

![](https://docs.streamlit.io/images/knowledge-base/chat-message-hello.png)

  

Notice the message is displayed with a default avatar and styling since we passed in `"user"` as the author name. You can also pass in `"assistant"` as the author name to use a different default avatar and styling, or pass in a custom name and avatar. See the [API reference](https://docs.streamlit.io/develop/api-reference/chat/st.chat_message) for more details.

`import streamlit as st import numpy as np with st.chat_message("assistant"): st.write("Hello human") st.bar_chart(np.random.randn(30, 3))`

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-message-user1.streamlit.app/?utm_medium=oembed)

While we've used the preferred `with` notation in the above examples, you can also just call methods directly in the returned objects. The below example is equivalent to the one above:

`import streamlit as st import numpy as np message = st.chat_message("assistant") message.write("Hello human") message.bar_chart(np.random.randn(30, 3))`

So far, we've displayed predefined messages. But what if we want to display messages based on user input?

### [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#stchat_input)st.chat_input

`st.chat_input` lets you display a chat input widget so the user can type in a message. The returned value is the user's input, which is `None` if the user hasn't sent a message yet. You can also pass in a default prompt to display in the input widget. Here's an example of how to use `st.chat_input` to display a chat input widget and show the user's input:

`import streamlit as st prompt = st.chat_input("Say something") if prompt: st.write(f"User has sent the following prompt: {prompt}")`

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-input.streamlit.app/?utm_medium=oembed)

Pretty straightforward, right? Now let's combine `st.chat_message` and `st.chat_input` to build a bot the mirrors or echoes your input.

## [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-bot-that-mirrors-your-input)Build a bot that mirrors your input

In this section, we'll build a bot that mirrors or echoes your input. More specifically, the bot will respond to your input with the same message. We'll use `st.chat_message` to display the user's input and `st.chat_input` to accept user input. We'll also use [session state](https://docs.streamlit.io/develop/concepts/architecture/session-state) to store the chat history so we can display it in the chat message container.

First, let's think about the different components we'll need to build our bot:

- Two chat message containers to display messages from the user and the bot, respectively.
- A chat input widget so the user can type in a message.
- A way to store the chat history so we can display it in the chat message containers. We can use a list to store the messages, and append to it every time the user or bot sends a message. Each entry in the list will be a dictionary with the following keys: `role` (the author of the message), and `content` (the message content).

`import streamlit as st st.title("Echo Bot") # Initialize chat history if "messages" not in st.session_state: st.session_state.messages = [] # Display chat messages from history on app rerun for message in st.session_state.messages: with st.chat_message(message["role"]): st.markdown(message["content"])`

In the above snippet, we've added a title to our app and a for loop to iterate through the chat history and display each message in the chat message container (with the author role and message content). We've also added a check to see if the `messages` key is in `st.session_state`. If it's not, we initialize it to an empty list. This is because we'll be adding messages to the list later on, and we don't want to overwrite the list every time the app reruns.

Now let's accept user input with `st.chat_input`, display the user's message in the chat message container, and add it to the chat history.

`# React to user input if prompt := st.chat_input("What is up?"): # Display user message in chat message container with st.chat_message("user"): st.markdown(prompt) # Add user message to chat history st.session_state.messages.append({"role": "user", "content": prompt})`

We used the `:=` operator to assign the user's input to the `prompt` variable and checked if it's not `None` in the same line. If the user has sent a message, we display the message in the chat message container and append it to the chat history.

All that's left to do is add the chatbot's responses within the `if` block. We'll use the same logic as before to display the bot's response (which is just the user's prompt) in the chat message container and add it to the history.

`response = f"Echo: {prompt}" # Display assistant response in chat message container with st.chat_message("assistant"): st.markdown(response) # Add assistant response to chat history st.session_state.messages.append({"role": "assistant", "content": response})`

Putting it all together, here's the full code for our simple chatbot GUI and the result:

View full code_expand_more_

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-echo.streamlit.app/?utm_medium=oembed)

While the above example is very simple, it's a good starting point for building more complex conversational apps. Notice how the bot responds instantly to your input. In the next section, we'll add a delay to simulate the bot "thinking" before responding.

## [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming)Build a simple chatbot GUI with streaming

In this section, we'll build a simple chatbot GUI that responds to user input with a random message from a list of pre-determind responses. In the [next section](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app), we'll convert this simple toy example into a ChatGPT-like experience using OpenAI.

Just like previously, we still require the same components to build our chatbot. Two chat message containers to display messages from the user and the bot, respectively. A chat input widget so the user can type in a message. And a way to store the chat history so we can display it in the chat message containers.

Let's just copy the code from the previous section and add a few tweaks to it.

`import streamlit as st import random import time st.title("Simple chat") # Initialize chat history if "messages" not in st.session_state: st.session_state.messages = [] # Display chat messages from history on app rerun for message in st.session_state.messages: with st.chat_message(message["role"]): st.markdown(message["content"]) # Accept user input if prompt := st.chat_input("What is up?"): # Display user message in chat message container with st.chat_message("user"): st.markdown(prompt) # Add user message to chat history st.session_state.messages.append({"role": "user", "content": prompt})`

The only difference so far is we've changed the title of our app and added imports for `random` and `time`. We'll use `random` to randomly select a response from a list of responses and `time` to add a delay to simulate the chatbot "thinking" before responding.

All that's left to do is add the chatbot's responses within the `if` block. We'll use a list of responses and randomly select one to display. We'll also add a delay to simulate the chatbot "thinking" before responding (or stream its response). Let's make a helper function for this and insert it at the top of our app.

`# Streamed response emulator def response_generator(): response = random.choice( [ "Hello there! How can I assist you today?", "Hi, human! Is there anything I can help you with?", "Do you need help?", ] ) for word in response.split(): yield word + " " time.sleep(0.05)`

Back to writing the response in our chat interface, we'll use `st.write_stream` to write out the streamed response with a typewriter effect.

`# Display assistant response in chat message container with st.chat_message("assistant"): response = st.write_stream(response_generator()) # Add assistant response to chat history st.session_state.messages.append({"role": "assistant", "content": response})`

Above, we've added a placeholder to display the chatbot's response. We've also added a for loop to iterate through the response and display it one word at a time. We've added a delay of 0.05 seconds between each word to simulate the chatbot "thinking" before responding. Finally, we append the chatbot's response to the chat history. As you've probably guessed, this is a naive implementation of streaming. We'll see how to implement streaming with OpenAI in the [next section](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app).

Putting it all together, here's the full code for our simple chatbot GUI and the result:

View full code_expand_more_

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-simple.streamlit.app/?utm_medium=oembed)

Play around with the above demo to get a feel for what we've built. It's a very simple chatbot GUI, but it has all the components of a more sophisticated chatbot. In the next section, we'll see how to build a ChatGPT-like app using OpenAI.

## [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app)Build a ChatGPT-like app

Now that you've understood the basics of Streamlit's chat elements, let's make a few tweaks to it to build our own ChatGPT-like app. You'll need to install the [OpenAI Python library](https://pypi.org/project/openai/) and get an [API key](https://platform.openai.com/account/api-keys) to follow along.

### [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#install-dependencies)Install dependencies

First let's install the dependencies we'll need for this section:

`pip install openai streamlit`

### [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#add-openai-api-key-to-streamlit-secrets)Add OpenAI API key to Streamlit secrets

Next, let's add our OpenAI API key to [Streamlit secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management). We do this by creating `.streamlit/secrets.toml` file in our project directory and adding the following lines to it:

`# .streamlit/secrets.toml OPENAI_API_KEY = "YOUR_API_KEY"`

### [](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#write-the-app)Write the app

Now let's write the app. We'll use the same code as before, but we'll replace the list of responses with a call to the OpenAI API. We'll also add a few more tweaks to make the app more ChatGPT-like.

`import streamlit as st from openai import OpenAI st.title("ChatGPT-like clone") # Set OpenAI API key from Streamlit secrets client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) # Set a default model if "openai_model" not in st.session_state: st.session_state["openai_model"] = "gpt-3.5-turbo" # Initialize chat history if "messages" not in st.session_state: st.session_state.messages = [] # Display chat messages from history on app rerun for message in st.session_state.messages: with st.chat_message(message["role"]): st.markdown(message["content"]) # Accept user input if prompt := st.chat_input("What is up?"): # Add user message to chat history st.session_state.messages.append({"role": "user", "content": prompt}) # Display user message in chat message container with st.chat_message("user"): st.markdown(prompt)`

All that's changed is that we've added a default model to `st.session_state` and set our OpenAI API key from Streamlit secrets. Here's where it gets interesting. We can replace our emulated stream with the model's responses from OpenAI:

`# Display assistant response in chat message container with st.chat_message("assistant"): stream = client.chat.completions.create( model=st.session_state["openai_model"], messages=[ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages ], stream=True, ) response = st.write_stream(stream) st.session_state.messages.append({"role": "assistant", "content": response})`

Above, we've replaced the list of responses with a call to [`OpenAI().chat.completions.create`](https://platform.openai.com/docs/guides/text-generation/chat-completions-api). We've set `stream=True` to stream the responses to the frontend. In the API call, we pass the model name we hardcoded in session state and pass the chat history as a list of messages. We also pass the `role` and `content` of each message in the chat history. Finally, OpenAI returns a stream of responses (split into chunks of tokens), which we iterate through and display each chunk.

Putting it all together, here's the full code for our ChatGPT-like app and the result:

View full code_expand_more_

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen_open_in_new_](https://doc-chat-llm.streamlit.app/?utm_medium=oembed)

Congratulations! You've built your own ChatGPT-like app in less than 50 lines of code.

We're very excited to see what you'll build with Streamlit's chat elements. Experiment with different models and tweak the code to build your own conversational apps. If you build something cool, let us know on the [Forum](https://discuss.streamlit.io/c/streamlit-examples/9) or check out some other [Generative AI apps](https://streamlit.io/generative-ai) for inspiration. 🎈