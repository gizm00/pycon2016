from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.sampledata.us_counties import data as counties


def create_plot(ridb) :

	or_counties = {
	    code: county for code, county in counties.items() if county["state"] == "or"
	}

	county_xs = [county["lons"] for county in or_counties.values()]
	county_ys = [county["lats"] for county in or_counties.values()]

	county_names = [county['name'] for county in or_counties.values()]


	lat = ridb['FacilityLatitude']
	lon = ridb['FacilityLongitude']

	source = ColumnDataSource(data=dict(
	    x=county_xs,
	    y=county_ys,
	    name=ridb['FacilityName']
	))

	TOOLS="pan,wheel_zoom,box_zoom,reset,save"

	ridb = ridb.assign(Secret = "TRILLIUM")

	df_source = ColumnDataSource(data=ridb[['FacilityName','FacilityPhone','Secret']])
	p = figure(title="Oregon Counties", tools=TOOLS)

	p.circle(lon, lat, size=8, color='navy', alpha=1, source=df_source, name='geo_points')

	p.patches('x', 'y', source=source,
	          fill_color='green', fill_alpha=0.7,
	          line_color="black", line_width=0.5)



	hover = HoverTool(names=['geo_points'])
	hover.tooltips = [(c, '@' + c) for c in ridb[['FacilityName','FacilityPhone','Secret']].columns]
	p.add_tools(hover)

	return p