from booking.booking import Booking

with Booking(teardown = False) as bot:
    bot.get_first_page()
    print("Closing the browser")
    # bot.sign_in()
    bot.select_place_to_go()
    i = 0
    no_of_pages_to_scrape = int(2)
    while i < no_of_pages_to_scrape:
        bot.get_hotels_info()
        i = i + 1

    bot.create_dataframe()
