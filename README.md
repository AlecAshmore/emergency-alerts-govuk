# notifications-govuk-alerts

## Setting up

### Python version

At the moment we run Python 3.6 in production.

### NPM packages

```shell
brew install node
```

[NPM](npmjs.org) is Node's package management tool. `n` is a tool for managing different versions of Node. The following installs `n` and uses the long term support (LTS) version of Node.

```shell
npm install -g n
n lts
```
## To run the application

```shell
# install dependencies, etc.
make bootstrap

# run the web app
make run-flask
```

Then visit [localhost:5000/alerts](http://localhost:5000/alerts).

Any Python code changes you make should be picked up automatically in development. If you're developing JavaScript code, run `npm run watch` to achieve the same.

## To test the application

```
# install dependencies, etc.
make bootstrap

# run all the tests
make test

# continuously run js tests
npm run test-watch
```

To run a specific JavaScript test, you'll need to copy the full command from `package.json`.o run a specific JavaScript test, you'll need to copy the full command from `package.json`.

## Browser support

We aim to match the [browsers supported by GOVUK Frontend](https://github.com/alphagov/govuk-frontend#browser-and-assistive-technology-support) (includes Internet Explorer 8-10).

## Further documentation

- [Image optimisation](docs/image-optimisation.md)
