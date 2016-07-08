restrictions  = {
	"calories": 2000,
	"micronutrients": {
		"protein-g":{"min":46, "max":56},
		"protein-p":{"min":10, "max"35},
		"carbonhydrate-g":130,
		"carbonhydrate-p":{"min":45, "max":65},
		"dietry-fibers":{"min":22, "max":33},
		"sugars-p":{"max":10},
		"fat-p":{"min":20, "max":35},
		"saturated-fat-p":{"max":10}
	}
}

# in the future this will recieve age, sex and activity level and will return smart restrictions
def get_restrictions():
	return restrictions