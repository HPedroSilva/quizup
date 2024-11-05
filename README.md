# QuizUp

> Interactive quiz that encourages players to enhance their knowledge in a competitive environment.

This project is a gamified quiz platform designed to promote learning in a fun and interactive way. Users can choose from various topics to answer questions or even create their own questions to challenge other players while learning a specific topic. The competition, whether between friends or against the system itself, aims to make learning more dynamic and engaging, encouraging curiosity and deepening knowledge.

The platform is currently being developed using Python with the Django framework for the backend and Bootstrap for the frontend. In future phases, the frontend will be restructured using React to offer a richer and more interactive user experience, while the Django REST Framework will be integrated into the backend to provide an API.

This project also serves as a practical ground for implementing complementary technologies such as Continuous Integration/Continuous Deployment (CI/CD) and linting practices to ensure code quality. The goal is to integrate automation and deployment tools to improve the platform's scalability and maintainability, as well as to explore the use of APIs.

## Project Usage Guidelines

### Dependency Management

This project utilizes `pipenv` for dependency management.

In addition, `pipenv` offers a `scripts` feature that is extensively used throughout this project. To view a complete list of available scripts, run the command:

```bash
pipenv scripts
```

### Commits

This project follows the `Conventional Commits` standard for commit messages to ensure consistency and readability. To simplify the commit process, it uses `commitizen` as a commit tool. Use the following command to create commits:

```bash
cz commit
```

Additionally, the project utilizes `commitlint` to check that commit messages adhere to the Conventional Commits standard, and `pre-commit` to automatically run validations before each commit.

To set up all necessary tools for the first time, run:

```bash
pipenv run init
```