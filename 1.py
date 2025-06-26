FILENAME = 'movies.csv'
WATCHED = 'w'
UNWATCHED = 'u'
CATEGORIES = ['Action', 'Comedy', 'Documentary', 'Drama', 'Thriller', 'Other']


def main():
    print("Must-See Movies 1.0 - by YOUR NAME HERE")
    movies = load_movies(FILENAME)
    print(f"{len(movies)} movies loaded from {FILENAME}")
    menu_choice = ""
    while menu_choice != 'Q':
        menu_choice = display_menu()
        if menu_choice == 'D':
            display_movies(movies)
        elif menu_choice == 'A':
            add_movie(movies)
        elif menu_choice == 'W':
            watch_movie(movies)
        elif menu_choice == 'Q':
            save_movies(FILENAME, movies)
            print(f"{len(movies)} movies saved to {FILENAME}")
            print("Have a nice day :)")
        else:
            print("Invalid menu choice")
def load_movies(filename):
    movies = []
    with open(filename, 'r') as file:
        for line in file:
            title, year, category, status = line.strip().split(',')
            movies.append([title, int(year), category, status])
    return movies

def save_movies(filename, movies):

    sorted_movies = sorted(movies, key=sort_key)
    with open(filename, 'w') as file:
        for movie in sorted_movies:
            file.write(f"{movie[0]},{movie[1]},{movie[2]},{movie[3]}\n")

def get_non_blank_input(prompt):
    response = input(prompt).strip()
    while response == '':
        print("Input can not be blank")
        response = input(prompt).strip()
    return response

def display_movies(movies):
    movies = sorted(movies, key=sort_key)
    watched_count = 0
    unwatched_count = 0
    for i in range(len(movies)):
        movie = movies[i]
        mark = '*' if movie[3] == UNWATCHED else ' '

        print(f"{i+1:2}. {mark} {movie[0]:35} - {movie[1]:4} ({movie[2]})")
        if movie[3] == WATCHED:
            watched_count += 1
        else:
            unwatched_count += 1
    print(f"{watched_count} movies watched. {unwatched_count} movies still to watch.")

def sort_key(movie):
    return (movie[1], movie[0])

def add_movie(movies):
    title = get_non_blank_input("Title: ")
    year = get_positive_integer("Year: ")
    print("Categories available: Action, Comedy, Documentary, Drama, Thriller, Other")
    category = input("Category: ").strip()
    while category == '':
        print("Input can not be blank")
        category = input("Category: ").strip()
    matched = False
    for valid in CATEGORIES:
        if valid.lower() == category.lower():
            category = valid
            matched = True
            break
    if not matched:
        print("Invalid category; using Other")
        category = 'Other'
    movies.append([title, year, category, UNWATCHED])
    print(f"{title} ({category} from {year}) added to movie list")
def watch_movie(movies):
    # 统计还没看的电影数量
    unwatched_count = sum(1 for m in movies if m[3] == UNWATCHED)
    if unwatched_count == 0:
        print("No more movies to watch!")
        return

    # 排序并显示
    sorted_movies = sorted(movies, key=sort_key)

    # 读第一行输入
    choice_input = input("Enter the movie number to mark watched.\n>>> ").strip()

    # 循环直到输入是 1..len(sorted_movies) 的数字
    while not (
        choice_input.lstrip('-').isdigit() and
        1 <= int(choice_input) <= len(sorted_movies)
    ):
        if not choice_input.lstrip('-').isdigit():
            print("Invalid input; enter a valid number")
        else:
            num = int(choice_input)
            if num < 1:
                print("Number must be >= 1")
            else:
                print("Invalid movie number.")
        choice_input = input(">>> ").strip()

    # 输入合法
    choice = int(choice_input)
    movie = sorted_movies[choice - 1]
    # 根据状态区分输出
    if movie[3] == WATCHED:
        # 已经是 w，就不改状态，只提示
        print(f"You have already watched {movie[0]}.")
    else:
        # 首次标记为已看
        movie[3] = WATCHED
        print(f"{movie[0]} ({movie[1]}) watched.")

def get_valid_input():
    return None

def display_menu():
    print("Menu:")
    print("D - Display movies")
    print("A - Add new movie")
    print("W - Watch a movie")
    print("Q - Quit")
    return input(">>> ").strip().upper()

def get_positive_integer(prompt):
    valid = False
    while not valid:
        try:
            number = int(input(prompt))
            if number >= 1:
                valid = True
            else:
                print("Number must be >= 1")
        except ValueError:
            print("Invalid input; enter a valid number")
    return number

main()
