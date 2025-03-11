import React, { useState, useEffect } from "react";
import {
  Container,
  ListGroup,
  Form,
  Button,
  InputGroup,
  Alert,
  Card,
  Modal,
  Spinner,
} from "react-bootstrap";

const IssueList = () => {
  const [issues, setIssues] = useState([]);
  const [newIssueDescription, setNewIssueDescription] = useState("");
  const [newIssueLocation, setNewIssueLocation] = useState("");
  const [newIssueAction, setNewIssueAction] = useState("");
  const [newIssuePropertyId, setNewIssuePropertyId] = useState("");
  const [editIssue, setEditIssue] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch issues on component mount
  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/issues/", {
        method: "GET",
        mode: "cors",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Fetched issues:", data);
      setIssues(data);
      setError(null);
    } catch (err) {
      console.error("Error fetching issues:", err);
      setError("Failed to load issues. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      newIssueDescription.trim() === "" ||
      newIssueLocation.trim() === "" ||
      newIssueAction.trim() === ""
    )
      return;

    try {
      // Create URL with query parameters
      const url = new URL("http://localhost:8000/issues/");
      url.searchParams.append("description", newIssueDescription.trim());
      url.searchParams.append("location", newIssueLocation.trim());
      url.searchParams.append("action", newIssueAction.trim());
      url.searchParams.append("resolved", "false");

      // Add property_id if provided
      if (newIssuePropertyId.trim() !== "") {
        url.searchParams.append("property_id", newIssuePropertyId.trim());
      }

      console.log("Sending request to:", url.toString());

      const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const newIssue = await response.json();
      setIssues([...issues, newIssue]);
      setNewIssueDescription("");
      setNewIssueLocation("");
      setNewIssueAction("");
      setNewIssuePropertyId("");
      setShowCreate(false);
      setError(null);
    } catch (err) {
      console.error("Error creating issue:", err);
      setError("Failed to create issue. Please try again.");
    }
  };

  const handleResolve = async (id) => {
    try {
      const url = new URL(`http://localhost:8000/issues/${id}`);
      url.searchParams.append("resolved", "true");

      const response = await fetch(url, {
        method: "PUT",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const updatedIssue = await response.json();
      setIssues(
        issues.map((issue) => (issue.id === id ? updatedIssue : issue))
      );
      setError(null);
    } catch (err) {
      console.error("Error resolving issue:", err);
      setError("Failed to resolve issue. Please try again.");
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/issues/${id}`, {
        method: "DELETE",
        mode: "cors",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      setIssues(issues.filter((issue) => issue.id !== id));
      setError(null);
    } catch (err) {
      console.error("Error deleting issue:", err);
      setError("Failed to delete issue. Please try again.");
    }
  };

  const handleEdit = (issue) => {
    setEditIssue(issue);
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      const url = new URL(`http://localhost:8000/issues/${editIssue.id}`);
      url.searchParams.append("description", editIssue.description);
      url.searchParams.append("location", editIssue.location);
      url.searchParams.append("action", editIssue.action);
      url.searchParams.append("resolved", editIssue.resolved.toString());

      if (editIssue.property_id) {
        url.searchParams.append("property_id", editIssue.property_id);
      }

      const response = await fetch(url, {
        method: "PUT",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const updatedIssue = await response.json();
      setIssues(
        issues.map((issue) =>
          issue.id === editIssue.id ? updatedIssue : issue
        )
      );
      setShowModal(false);
      setEditIssue(null);
      setError(null);
    } catch (err) {
      console.error("Error updating issue:", err);
      setError("Failed to update issue. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="issue-list">
        <Card.Header>Issue List</Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}

          {loading ? (
            <div className="text-center">
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : issues.length === 0 ? (
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
                    <div>Status: {issue.resolved ? "Resolved" : "Open"}</div>
                  </div>
                  <div>
                    {!issue.resolved ? (
                      <Button
                        variant="success"
                        size="sm"
                        onClick={() => handleResolve(issue.id)}
                      >
                        Resolve
                      </Button>
                    ) : (
                      <>
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => handleEdit(issue)}
                          className="me-2"
                        >
                          Edit
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => handleDelete(issue.id)}
                        >
                          Delete
                        </Button>
                      </>
                    )}
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
          <br />
          <Button
            variant="secondary"
            onClick={() => setShowCreate(!showCreate)}
          >
            {showCreate ? "Cancel" : "Create"}
          </Button>
          {showCreate && (
            <Form onSubmit={handleSubmit} className="mb-4 mt-3">
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
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newIssuePropertyId}
                  onChange={(e) => setNewIssuePropertyId(e.target.value)}
                  placeholder="Enter property ID (optional)"
                />
              </InputGroup>
              <Button variant="primary" type="submit">
                Add Issue
              </Button>
            </Form>
          )}
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Issue</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editIssue?.description || ""}
                onChange={(e) =>
                  setEditIssue({ ...editIssue, description: e.target.value })
                }
                placeholder="Enter issue description"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editIssue?.location || ""}
                onChange={(e) =>
                  setEditIssue({ ...editIssue, location: e.target.value })
                }
                placeholder="Enter issue location"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editIssue?.action || ""}
                onChange={(e) =>
                  setEditIssue({ ...editIssue, action: e.target.value })
                }
                placeholder="Enter action to take"
              />
            </InputGroup>
            <Form.Check
              type="checkbox"
              label="Resolved"
              checked={editIssue?.resolved || false}
              onChange={(e) =>
                setEditIssue({ ...editIssue, resolved: e.target.checked })
              }
              className="mb-3"
            />
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default IssueList;
