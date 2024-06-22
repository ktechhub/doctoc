<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*

<!---toc start-->

* [Contribution Guidelines](#contribution-guidelines)
    * [Reporting Issues](#reporting-issues)
    * [Forking the Repository](#forking-the-repository)
    * [Making Changes](#making-changes)
    * [Commit Prefixes](#commit-prefixes)
    * [Submitting a Pull Request](#submitting-a-pull-request)
    * [Code Style and Testing](#code-style-and-testing)
    * [Documentation](#documentation)
    * [Testing](#testing)
    * [License](#license)

<!---toc end-->

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
# Contribution Guidelines

We welcome contributions from the community to help improve this project. Below are the guidelines for contributing:

### Reporting Issues

If you encounter any issues or bugs, please report them by opening an issue on the [GitHub Issues](https://github.com/ktechhub/doctoc/issues) page. Provide as much detail as possible, including steps to reproduce the issue and any relevant logs.

### Forking the Repository

1. Fork the repository by clicking on the "Fork" button at the top right of the repository page.
2. Clone your forked repository to your local machine:
    ```sh
    git clone https://github.com/your-username/doctoc.git
    ```
3. Navigate to the project directory:
    ```sh
    cd doctoc
    ```

### Making Changes

1. Create a new branch for your changes:
    ```sh
    git checkout -b feature/your-feature-name
    ```
2. Make your changes to the codebase.
3. Commit your changes with a descriptive commit message:
    ```sh
    git commit -m "feat: description of your feature"
    ```
4. Push your changes to your forked repository:
    ```sh
    git push origin feature/your-feature-name
    ```

### Commit Prefixes

When making commits, please use the following prefixes to categorize your changes:

- `feat:` for new features
- `fix:` for bug fixes
- `hotfix:` for critical hotfixes
- `refactor:` for code refactoring that does not add new features or fix bugs
- `docs:` for changes to documentation
- `style:` for formatting changes that do not affect the meaning of the code (e.g., linting)
- `test:` for adding or updating tests
- `chore:` for other changes that do not modify `src` or `test` files (e.g., updating build scripts)
- `perf:` for performance improvements
- `ci:` for changes to the CI configuration files and scripts
- `build:` for changes that affect the build system or external dependencies

These prefixes help maintain a clear and organized commit history.

### Submitting a Pull Request

1. Once your changes are pushed to your forked repository, navigate to the original repository.
2. Click on the "Pull Requests" tab and then click the "New Pull Request" button.
3. Select your feature branch from the "compare" dropdown, and ensure the base repository is set to the original repository.
4. Provide a detailed description of your changes and submit the pull request.

### Code Style and Testing

We use Black for code formatting. Ensure you run Black on your code before submitting a pull request:

```sh
black .
```

### Documentation

- Update documentation to reflect any changes made in the codebase.
- Ensure docstrings are provided for functions, classes, and modules.

### Testing

- Please ensure your code is well-documented and write tests with pytest.

### License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for your contributions!