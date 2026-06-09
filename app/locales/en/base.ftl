# Navigation
common-back = ⬅️ Back
items-end = ⏩
items-start = ⏪
items-back = ⬅️
items-forward = ➡️

# Main Menu
main-menu-text =
    🏠 Main Menu
    Choose action:

main-menu-welcome =
    🏠 Main Menu
    Welcome to the bot with
    lots of resources on
    programming, web, cybersecurity, etc.
    Choose action:

main-menu-keyboard-resources = 🗂️ Resources
main-menu-keyboard-search-resource = 🔍 Search
main-menu-keyboard-favorite = ⭐ Favorite
main-menu-keyboard-manage-resources = 🛠️ Manage resources
main-menu-keyboard-manage-categories = ⚙️ Manage categories
main-menu-keyboard-manage-users = 👤 Manage users
main-menu-keyboard-manage-quizes = 👔 Manage quizes

# Manage Resources
manage-resources-text =
    🛠️ Manage Resources
    Choose action:

manage-resources-keyboard-create = ➕ Create Resource
manage-resources-keyboard-edit = ✏️ Edit Resource
manage-resources-keyboard-delete = 🗑️ Delete Resource

manage-resources-create-choose-category = 📤 Select category
manage-resources-create-wait-name = 📤 Send resource name
manage-resources-create-wait-description = 📤 Send resource description
manage-resources-create-wait-images = 📤 Send resource images
manage-resources-create-wait-links = 📤 Send resource links
manage-resources-create-wait-tags = 📤 Send resource tags

manage-resources-create-success =
    ✅ Resource created successfully

    Resource name: { $resource_name }

    Category name: { $category_name }

    Resource description: { $resource_description }

    Resource tags: { $resource_tags }

manage-resources-create-fail =
    ❌ Resource with this name already exists or something went wrong

    Resource name: { $resource_name }

    Category name: { $category_name }

    Resource description: { $resource_description }

    Resource tags: { $resource_tags }

manage-resources-create-no-categories = ❌ No categories

manage-resources-edit-choose-resource = 📤 Select resource
manage-resources-edit-choose-category = 📤 Select resource category
manage-resources-edit-choose-to-change = 📤 Choose what to edit
manage-resources-edit-name-choose = ✏️ Edit name
manage-resources-edit-description-choose = 📝 Edit description
manage-resources-edit-image-choose = 🖼️ Edit image
manage-resources-edit-tags-choose = 🏷️ Edit tags

manage-resources-edit-name-text =
    ✏️ Send new resource name

    Resource name: { $name }

manage-resources-edit-description-text =
    📝 Send new resource description

    Resource description: { $description }

manage-resources-edit-image-text = 🖼️ Send new resource image

manage-resources-edit-tags-text =
    🏷️ Send new resource tags

    Resource tags: { $tags }

manage-resources-edit-name-success =
    ✅ Resource name changed succesfully

    Resource name: { $name }

manage-resources-edit-description-success =
    ✅ Resource description changed successfully

    Resource description: { $description }

manage-resources-edit-image-success = ✅ Resource image changed succesfully

manage-resources-edit-tags-success =
    ✅ Resource tags changed successfully

    Resource tags: { $tags }

manage-resources-edit-name-fail =
    ❌ Resource with this name already exists or something went wrong

    Resource name: { $resource_name }

manage-resources-edit-description-fail =
    ❌ Description doesn't change. Something went wrong

    Resource description: { $resource_description }

manage-resources-edit-image-fail = ❌ Image doesn't change. Something went wrong

manage-resources-edit-tags-fail =
    ❌ Tags doesn't change. Something went wrong

    Resource tags: { $tags }

manage-resources-edit-no-resources = ❌ No resources in this category
manage-resources-edit-no-categories = ❌ No categories

manage-resources-delete-choose-category = 📤 Select resource category
manage-resources-delete-choose-resource = 📤 Select resource to delete

manage-resources-delete-choose-to-delete =
    📤 Are you sure?

    Resource will be deleted:
    Resource name: { $name }

manage-resources-delete-confirm = ❌ Delete resource

manage-resources-delete-success =
    ✅ Resource deleted

    Resource name: { $name }

manage-resources-delete-fail =
    ❌ Resource doesn't deleted. Something went wrong

    Resource name: { $name }

manage-resources-delete-no-resources = ❌ No resources in this category
manage-resources-delete-no-categories = ❌ No categories

# Manage Categories
manage-categories-text =
    🛠️ Manage Categories
    Choose action:

manage-categories-keyboard-create = ➕ Create Category
manage-categories-keyboard-edit = ✏️ Edit Category
manage-categories-keyboard-delete = 🗑️ Delete Category

manage-categories-create-text = 📤 Send category name

manage-categories-create-success =
    ✅ Category created successfully

    Category name: { $category_name }

manage-categories-create-fail =
    ❌ Category with this name already exists

    Category name: { $category_name }

manage-categories-create-no-resources = ❌ No resources in this category
manage-categories-create-no-categories = ❌ No categories

manage-categories-edit-choose = 📤 Choose category to edit
manage-categories-edit-text = 📤 Send new category name

manage-categories-edit-success =
    ✅ Category name changed successfully

    Category name: { $category_name }

manage-categories-edit-fail =
    ❌ Category with this name already exists

    Category name: { $category_name }

manage-categories-edit-no-resources = ❌ No resources in this category
manage-categories-edit-no-categories = ❌ No categories

manage-categories-delete-choose = 📤 Choose category to delete

manage-categories-delete-success =
    ✅ Category deleted successfully

    Category name: { $category_name }

manage-categories-delete-fail =
    ❌ Category with this name already deleted or something went wrong

    Category name: { $category_name }

manage-categories-delete-no-resources = ❌ No resources in this category
manage-categories-delete-no-categories = ❌ No categories

# Manage Quizes
manage-quizes-text =
    🛠️ Manage Quizes
    Choose action:

manage-quizes-keyboard-create = ➕ Create Quiz
manage-quizes-keyboard-edit = ✏️ Edit Quiz
manage-quizes-keyboard-delete = 🗑️ Delete Quiz

manage-quizes-create-choose-category = 📤 Select category to create quiz
manage-quizes-create-choose = 📤 Select resource
manage-quizes-create-wait-quiz = 📤 Send quiz name or info

manage-quizes-create-send-question =
    📤 Send question in format:
    question text on first line
    each option on separate line
    prefix correct options with !

manage-quizes-create-add-question = ➕ Add another question or finish

manage-quizes-create-fail =
    ❌ Failed to create quiz

    Resource name: { $resource_name }
    Question count: { $question_count }

manage-quizes-create-success =
    ✅ Quiz created successfully

    Resource name: { $resource_name }
    Question count: { $question_count }

manage-quizes-create-no-resources = ❌ No resources in this category
manage-quizes-create-no-categories = ❌ No categories
manage-quizes-create-stop-questions = ✅ Finish creating quiz

manage-quizes-delete-choose-category = 📤 Select category to delete quiz
manage-quizes-delete-choose-resource = 📤 Select resource to delete quiz

manage-quizes-delete-success =
    ✅ Quiz deleted successfully

    Quiz name: { $resource_name }

manage-quizes-delete-fail =
    ❌ Resource with this name already deleted or something went wrong

    Resource name: { $resource_name }

manage-quizes-delete-choose-to-delete =
    📤 Are you sure?

    Quiz will be deleted:
    Resource name: { $name }

manage-quizes-delete-confirm = ❌ Delete quiz
manage-quizes-delete-no-resources = ❌ No resources in this category
manage-quizes-delete-no-categories = ❌ No categories

manage-quizes-edit-choose-category = 📤 Select category to edit quiz
manage-quizes-edit-choose-resource = 📤 Select resource to edit quiz
manage-quizes-edit-no-categories = ❌ No categories
manage-quizes-edit-choose-to-change = 📤 Choose what to edit
manage-quizes-keyboard-delete-question = ❌ Delete question
manage-quizes-keyboard-edit-question = ✏️ Edit question
manage-quizes-keyboard-add-question = ➕ Add question

manage-quizes-edit-delete-question-number =
    Enter question number to delete:

    { $questions }

manage-quizes-edit-delete-question-fail = ❌ Quiz question with this number already deleted or something went wrong
manage-quizes-edit-delete-question-success = ✅ Quiz question deleted successfully
manage-quizes-edit-add-question-fail = ❌ Something went wrong with creating this quiz question
manage-quizes-edit-add-question-success = ✅ Quiz question added successfully

manage-quizes-edit-add-question-text =
    Enter new question to add:

    { $questions }

manage-quizes-edit-edit-question-number =
    Enter question number to edit:

    { $questions }

manage-quizes-edit-edit-question-text = Enter new question text
manage-quizes-edit-edit-question-success = ❌ Something went wrong with editing this quiz question
manage-quizes-edit-edit-question-fail = ✅ Quiz question updated successfully

# List Resources
list-resources-choose-category = 📤 Select category
list-resources-choose-resource = 📤 Select resource
list-resources-change-page = 📤 Select resource

list-resources-start-quiz-question =
    ✏️ Start quiz?

    Resource name: { $resource_name }
    Question count: { $question_count }

list-resources-start-quiz-confirm = ✅ Start quiz

# List Favorites
list-favorites-choose-category = 📤 Select category
list-favorites-choose-resource = 📤 Select resource
list-favorites-change-page = 📤 Select resource
list-favorites-no-results = ❌ You doesn't have resources in favorites yet

# Search
search-resource-enter-text = ✏️ Enter resource text, tags or description
search-resource-select = ✏️ Select the appropriate resource

# Manage Users
manage-users-text =
    🛠️ Manage Users
    Choose action:

manage-users-keyboard-edit = ✏️ Edit User
manage-users-keyboard-block = 🗑️ Block User

# Favorites
favorite-add = ✅ Add to favorite
favorite-remove = ❌ Remove from favorite

# Quiz
start-quiz-completed = 🔄 Retry Quiz ({ $current_percent }%)
start-quiz-retry = 🔄 Retry Quiz
start-quiz-firstly = 📝 Start Quiz
start-quiz-final = ✅ You pass quiz. Your result is { $percent }%. Retry?
