import util
global FileNames

FileNames={
	'business':util.getAbsFileName('data/yelp_Academic_dataset_business.json'),
	'review':util.getAbsFileName('data/yelp_Academic_dataset_review.json'),
	'user':util.getAbsFileName('data/yelp_Academic_dataset_user.json'),
	'checkin':util.getAbsFileName('data/yelp_Academic_dataset_checkin.json'),
	'tip':util.getAbsFileName('data/yelp_Academic_dataset_tip.json'),
	'test': util.getAbsFileName('data/test.json'),
	'positive-words': util.getAbsFileName('data/positive-words.txt'),
	'negative-words': util.getAbsFileName('data/negative-words.txt'),
	'common-words': util.getAbsFileName('data/common-words.txt'),
	'reviews-train': util.getAbsFileName('data/reviews_train.txt'),
	'reviews-test': util.getAbsFileName('data/reviews_test.txt'),
	'reviews-test-perbusiness-perdate': util.getAbsFileName('data/reviews_test_perbusiness_perdate.txt'),
	'tips-test-perbusiness-perdate': util.getAbsFileName('data/tips_test_perbusiness_perdate.txt')
	}

