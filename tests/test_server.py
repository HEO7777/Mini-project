import pytest

def test_kill_process_no_data(client):
    """Test that sending no data returns a 400 error."""
    response = client.post('/api/process/kill', json={})
    assert response.status_code == 400

def test_kill_process_invalid_pid_type(client):
    """Test client-side verification: PID must be an integer."""
    response = client.post('/api/process/kill', json={'pid': 'abc'})
    assert response.status_code == 400
    assert b"Invalid PID" in response.data

def test_kill_process_protected_pid(client):
    """Test protection: PID 1 should never be killed."""
    response = client.post('/api/process/kill', json={'pid': 1})
    assert response.status_code == 403
    assert b"Protected process" in response.data

def test_kill_process_not_found(client):
    """Test handling of non-existent PIDs."""
    # Using a very high PID that likely doesn't exist
    response = client.post('/api/process/kill', json={'pid': 999999})
    assert response.status_code == 404