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

const PropertyList = () => {
  const [properties, setProperties] = useState([]);
  const [newPropertyAddress, setNewPropertyAddress] = useState("");
  const [newPropertyLandlordId, setNewPropertyLandlordId] = useState("");
  const [editProperty, setEditProperty] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch properties on component mount
  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/properties/", {
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
      console.log("Fetched properties:", data);
      setProperties(data);
      setError(null);
    } catch (err) {
      console.error("Error fetching properties:", err);
      setError("Failed to load properties. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPropertyAddress.trim() === "" || newPropertyLandlordId.trim() === "")
      return;

    try {
      // Create URL with query parameters instead of using JSON body
      const url = new URL("http://localhost:8000/properties/");
      url.searchParams.append("address", newPropertyAddress.trim());
      url.searchParams.append("landlord_id", newPropertyLandlordId.trim());

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

      const newProperty = await response.json();
      setProperties([...properties, newProperty]);
      setNewPropertyAddress("");
      setNewPropertyLandlordId("");
      setShowCreate(false);
      setError(null);
    } catch (err) {
      console.error("Error creating property:", err);
      setError("Failed to create property. Please try again.");
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/properties/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      setProperties(properties.filter((property) => property.id !== id));
      setError(null);
    } catch (err) {
      console.error("Error deleting property:", err);
      setError("Failed to delete property. Please try again.");
    }
  };

  const handleEdit = (property) => {
    setEditProperty(property);
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      const url = new URL(
        `http://localhost:8000/properties/${editProperty.id}`
      );
      url.searchParams.append("address", editProperty.address);
      url.searchParams.append("landlord_id", editProperty.landlord_id);

      const response = await fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const updatedProperty = await response.json();
      setProperties(
        properties.map((property) =>
          property.id === editProperty.id ? updatedProperty : property
        )
      );
      setShowModal(false);
      setEditProperty(null);
      setError(null);
    } catch (err) {
      console.error("Error updating property:", err);
      setError("Failed to update property. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <Card bg="dark" border="dark" text="white" className="property-list">
        <Card.Header>Property List</Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}

          {loading ? (
            <div className="text-center">
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : properties.length === 0 ? (
            <Alert variant="info">No properties in the list yet!</Alert>
          ) : (
            <ListGroup>
              {properties.map((property) => (
                <ListGroup.Item
                  key={property.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div>Address: {property.address}</div>
                    <div>Landlord ID: {property.landlord_id}</div>
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleEdit(property)}
                      className="me-2"
                    >
                      Edit
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(property.id)}
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
                  value={newPropertyAddress}
                  onChange={(e) => setNewPropertyAddress(e.target.value)}
                  placeholder="Enter property address"
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <Form.Control
                  type="text"
                  value={newPropertyLandlordId}
                  onChange={(e) => setNewPropertyLandlordId(e.target.value)}
                  placeholder="Enter landlord ID"
                />
              </InputGroup>
              <Button variant="primary" type="submit">
                Add Property
              </Button>
            </Form>
          )}
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Property</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editProperty?.address || ""}
                onChange={(e) =>
                  setEditProperty({
                    ...editProperty,
                    address: e.target.value,
                  })
                }
                placeholder="Enter property address"
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <Form.Control
                type="text"
                value={editProperty?.landlord_id || ""}
                onChange={(e) =>
                  setEditProperty({
                    ...editProperty,
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

export default PropertyList;
