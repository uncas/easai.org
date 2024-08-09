import React, { Component } from 'react';

export class Home extends Component {
  static displayName = Home.name;

  render() {
    const projects = [
      {
        name: "Python Automation, including AI agents",
        url: "https://github.com/uncas/Uncas.Automation"
      }
    ]
    return (
      <div className="App">
        <header className="App-header">
          <h2>
            Welcome to easai.org
          </h2>
          <p>
            We aim to leverage computers and automations to make our lives easier.
          </p>
          <p>
            We are currently working on:
          </p>
          {projects.map(project => (
            <div>
              <a
                className="App-link"
                href={project.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {project.name}
              </a>
            </div>
          ))}
        </header>
      </div>
    );
  }
}