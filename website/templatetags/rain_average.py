from django import template

register = template.Library()

@register.simple_tag
def get_rain_average(month_avg, month):
	
	return month_avg[month]['sum'] / month_avg[month]['count']