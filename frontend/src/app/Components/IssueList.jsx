import React, { useState } from "react";
import {
  Container,
  ListGroup,
  Form,
  Button,
  InputGroup,
  Alert,
  Card,
} from "react-bootstrap";

const IssueList = () => {
  const [issues, setIssues] = useState([]);
  const [newIssueDescription, setNewIssueDescription] = useState("");
  const [newIssueLocation, setNewIssueLocation] = useState("");
  const [newIssueAction, setNewIssueAction] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (
      newIssueDescription.trim() === "" ||
      newIssueLocation.trim() === "" ||
      newIssueAction.trim() === ""
    )
      return;

    setIssues([
      ...issues,
      {
        id: Date.now(),
        description: newIssueDescription.trim(),
        location: newIssueLocation.trim(),
        action: newIssueAction.trim(),
        resolved: false,
      },
    ]);
    setNewIssueDescription("");
    setNewIssueLocation("");
    setNewIssueAction("");
  };

  const handleResolve = (id) => {
    setIssues(
      issues.map((issue) =>
        issue.id === id ? { ...issue, resolved: true } : issue
      )
    );
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="issue-list">
        <Card.Header>Issue List</Card.Header>
        <Card.Body>
          {issues.length === 0 ? (
            <Alert variant="info">No issues in the list yet!</Alert>
          ) : (
            <ListGroup>
              {issues.map((issue) => (
                <ListGroup.Item
                  key={issue.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>Issue #: {issue.id}</div>
                    <div>Description: {issue.description}</div>
                    <div>Location: {issue.location}</div>
                    <div>Action: {issue.action}</div>
                  </div>
                  <div>
                    {!issue.resolved && (
                      <Button
                        variant="success"
                        size="sm"
                        onClick={() => handleResolve(issue.id)}
                      >
                        Resolve
                      </Button>
                    )}
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
          <br />
          <Form onSubmit={handleSubmit} className="mb-4">
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newIssueDescription}
                onChange={(e) => setNewIssueDescription(e.target.value)}
                placeholder="Enter issue description"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newIssueLocation}
                onChange={(e) => setNewIssueLocation(e.target.value)}
                placeholder="Enter issue location"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={newIssueAction}
                onChange={(e) => setNewIssueAction(e.target.value)}
                placeholder="Enter action to take"
              />
            </InputGroup>
            <Button variant="primary" type="submit">
              Add Issue
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default IssueList;
