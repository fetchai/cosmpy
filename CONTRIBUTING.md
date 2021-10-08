# Contributing

Contributions to this library are welcome.

- If you want to report a bug or ask for features, you can check the [Issues page](https://github.com/fetchai/cosmpy/issues) and raise an issue.

- If you would like to contribute a bug fix or feature then [submit a Pull request](https://github.com/fetchai/cosmpy/pulls).

For other kinds of feedback, you can contact one of the
[authors](https://github.com/fetchai/cosmpy/blob/main/AUTHORS.md) by email.

Before reading on, please have a look at the [code of conduct](https://github.com/fetchai/cosmpy/blob/main/CODE_OF_CONDUCT.md).

## A few simple rules

- All Pull Requests should be opened against the `develop` branch. Do **not** open a Pull Request against `main`!

- Before working on a feature, reach out to one of the core developers or discuss the feature in an issue. The framework caters a diverse audience and new features require upfront coordination.

- Include unit tests for 100% coverage when you contribute new features, as they help to a) prove that your code works correctly, and b) guard against future breaking changes to lower the maintenance cost.

- Bug fixes also generally require unit tests, because the presence of bugs usually indicates insufficient test coverage.

- Keep API compatibility in mind when you change code in `cosmpy`. Above version `1.0.0`, breaking changes can happen across versions with different left digit. Below version `1.0.0`, they can happen across versions with different middle digit. Reviewers of your pull request will comment on any API compatibility issues.
  
- When you contribute a new feature to `cosmpy`, the maintenance burden is transferred to the core team. This means that the benefit of the contribution must be compared against the cost of maintaining the feature.

- Where possible, extend existing features instead of replacing one. 

- All files must include a license header.

- Before committing and opening a PR, run all tests locally. This saves CI hours and ensures you only commit clean code.

## Contributing code

If you have improvements, send us your pull requests!

A team member will be assigned to review your pull requests. All tests are run as part of CI as well as various other checks (linters, static type checkers, security checkers, etc). If there are any problems, feedback is provided via GitHub. Once the pull requests is approved and passes continuous integration checks, you or a team member can merge it.

If you want to contribute, start working through the codebase, navigate to the Github [Issues page](https://github.com/fetchai/cosmpy/issues) tab and start looking through interesting issues. If you decide to start on an issue, leave a comment so that other people know that you're working on it. If you want to help out, but not alone, use the issue comment thread to coordinate.
