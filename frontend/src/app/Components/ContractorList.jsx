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

const ContractorList = () => {
  const [contractors, setContractors] = useState([]);
  const [newContractorName, setNewContractorName] = useState("");
  const [newContractorEmail, setNewContractorEmail] = useState("");
  const [newContractorPhone, setNewContractorPhone] = useState("");
  const [newContractorWork, setNewContractorWork] = useState("");
  const [newContractorLandlordId, setNewContractorLandlordId] = useState("");
  const [editContractor, setEditContractor] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch contractors on component mount
  useEffect(() => {
    fetchContractors();
  }, []);

  const fetchContractors = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/contractors/", {
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
      console.log("Fetched contractors:", data);
      setContractors(data);
      setError(null);
    } catch (err) {
      console.error("Error fetching contractors:", err);
      setError("Failed to load contractors. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      newContractorName.trim() === "" ||
      newContractorEmail.trim() === "" ||
      newContractorPhone.trim() === "" ||
      newContractorWork.trim() === ""
    )
      return;

    try {
      // Create URL with query parameters
      const url = new URL("http://localhost:8000/contractors/");
      url.searchParams.append("name", newContractorName.trim());
      url.searchParams.append("email", newContractorEmail.trim());
      url.searchParams.append("phone_number", newContractorPhone.trim());
      url.searchParams.append("work", newContractorWork.trim());

      // Add landlord_id if provided
      if (newContractorLandlordId.trim() !== "") {
        url.searchParams.append("landlord_id", newContractorLandlordId.trim());
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
        const errorData = await response.json().catch(() => null);
        console.error("Server response:", errorData);

        if (errorData && errorData.detail) {
          throw new Error(
            Array.isArray(errorData.detail)
              ? errorData.detail
                  .map((err) => `${err.loc.join(".")}: ${err.msg}`)
                  .join(", ")
              : errorData.detail
          );
        }
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const newContractor = await response.json();
      setContractors([...contractors, newContractor]);
      setNewContractorName("");
      setNewContractorEmail("");
      setNewContractorPhone("");
      setNewContractorWork("");
      setNewContractorLandlordId("");
      setShowCreate(false);
      setError(null);
    } catch (err) {
      console.error("Error creating contractor:", err);
      setError(`Failed to create contractor: ${err.message}`);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/contractors/${id}`, {
        method: "DELETE",
        mode: "cors",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      setContractors(contractors.filter((contractor) => contractor.id !== id));
      setError(null);
    } catch (err) {
      console.error("Error deleting contractor:", err);
      setError("Failed to delete contractor. Please try again.");
    }
  };

  const handleEdit = (contractor) => {
    setEditContractor(contractor);
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      const url = new URL(
        `http://localhost:8000/contractors/${editContractor.id}`
      );
      url.searchParams.append("name", editContractor.name);
      url.searchParams.append("email", editContractor.email);
      url.searchParams.append("phone_number", editContractor.phone_number);
      url.searchParams.append("work", editContractor.work);

      // Include landlord_id in the update if it exists
      if (editContractor.landlord_id) {
        url.searchParams.append("landlord_id", editContractor.landlord_id);
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

      const updatedContractor = await response.json();
      setContractors(
        contractors.map((contractor) =>
          contractor.id === editContractor.id ? updatedContractor : contractor
        )
      );
      setShowModal(false);
      setEditContractor(null);
      setError(null);
    } catch (err) {
      console.error("Error updating contractor:", err);
      setError("Failed to update contractor. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="contractor-list">
        <Card.Header>Contractor List</Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}

          {loading ? (
            <div className="text-center">
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : contractors.length === 0 ? (
            <Alert variant="info">No contractors in the list yet!</Alert>
          ) : (
            <ListGroup>
              {contractors.map((contractor) => (
                <ListGroup.Item
                  key={contractor.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>{contractor.name}</div>
                    <div>{contractor.email}</div>
                    <div>{contractor.phone_number}</div>
                    <div>{contractor.work}</div>
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleEdit(contractor)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(contractor.id)}
                    >
                      Delete
                    </Button>
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
                  value={newContractorName}
                  onChange={(e) => setNewContractorName(e.target.value)}
                  placeholder="Enter contractor name"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="email"
                  value={newContractorEmail}
                  onChange={(e) => setNewContractorEmail(e.target.value)}
                  placeholder="Enter contractor email"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newContractorPhone}
                  onChange={(e) => setNewContractorPhone(e.target.value)}
                  placeholder="Enter contractor phone"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newContractorWork}
                  onChange={(e) => setNewContractorWork(e.target.value)}
                  placeholder="Enter contractor work"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newContractorLandlordId}
                  onChange={(e) => setNewContractorLandlordId(e.target.value)}
                  placeholder="Enter landlord ID"
                />
              </InputGroup>
              <Button variant="primary" type="submit">
                Add Contractor
              </Button>
            </Form>
          )}
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Contractor</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.name || ""}
                onChange={(e) =>
                  setEditContractor({ ...editContractor, name: e.target.value })
                }
                placeholder="Enter contractor name"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="email"
                value={editContractor?.email || ""}
                onChange={(e) =>
                  setEditContractor({
                    ...editContractor,
                    email: e.target.value,
                  })
                }
                placeholder="Enter contractor email"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.phone_number || ""}
                onChange={(e) =>
                  setEditContractor({
                    ...editContractor,
                    phone_number: e.target.value,
                  })
                }
                placeholder="Enter contractor phone"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.work || ""}
                onChange={(e) =>
                  setEditContractor({ ...editContractor, work: e.target.value })
                }
                placeholder="Enter contractor work"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editContractor?.landlord_id || ""}
                onChange={(e) =>
                  setEditContractor({
                    ...editContractor,
                    landlord_id: e.target.value,
                  })
                }
                placeholder="Enter landlord ID"
              />
            </InputGroup>
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

export default ContractorList;
