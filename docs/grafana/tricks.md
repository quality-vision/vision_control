# Tricks
In this document will tranforms and other 'tricks' that was found especially helpful be presented.

## Transforms
These are the transforms that was experienced to be extra useful for good visualization.

### Rows to field
The transform `Rows to field` was frequently used, especially for all pie charts. The transform makes all rows in the response data to a seperate field. Each field can then be managed individually which enables the possibilites to map the values in the field to labels. These labels can help to make the visualization easier to understand and more self explaining. The transform uses one of the fields to retrive the name of the field and another field to retrive the value.

### Convert field type
With the transform `Convert Field Type` the type of a field can be changed. This can for example be helpful if a log contains a number but is treated as a string in the log. This is used in the `Sentry Events by Type` panel. Where the `Count` field originally is a string, but by using `Convert Field Type` and choose `Count` as `Numeric` it can be used as a number instead and the amount of all event types can be calculated.

### Organize fields
Some data sources doesn't allow overrides on its data. This means that the fields are very limited for customization and the visualization can therefore be confusing. The transform `Organize fields` can help to make the data cleaner and clearer. With the transorm fields can be re-ordered if the order is important. By marking the eye symbol next to the field name the field can be hidden if the field isn't necessary for the representation or renamed if another name is wished for in the panel.

## Debugging
If there is an error on a dashboard it is possible to get additional information about the error. This information is reached by clicking on the `Query Insepctor` button located in the top right corner of the query window beneath the panel. This will open a window that shows the raw data of the query. Sentry supplies an URL that contains an explanation of what went wrong.
