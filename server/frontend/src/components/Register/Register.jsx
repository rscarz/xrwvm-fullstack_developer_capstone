import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  // State variables
  const [formData, setFormData] = useState({
    userName: "",
    password: "",
    email: "",
    firstName: "",
    lastName: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Redirect to home
  const gohome = () => {
    window.location.href = window.location.origin;
  };

  // Handle form submission
  const register = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Basic validation
    const { userName, password, email, firstName, lastName } = formData;
    if (!userName || !password || !email || !firstName || !lastName) {
      setError("Por favor, complete todos los campos");
      setLoading(false);
      return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Por favor, ingrese un correo electrónico válido");
      setLoading(false);
      return;
    }

    try {
      const register_url = `${window.location.origin}/djangoapp/register`;

      const res = await fetch(register_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName,
          password,
          firstName,
          lastName,
          email
        }),
      });

      const json = await res.json();
      
      if (json.status) {
        sessionStorage.setItem('username', json.userName);
        window.location.href = window.location.origin;
      } else {
        setError(json.error || "Error en el registro. Por favor, intente de nuevo.");
      }
    } catch (err) {
      console.error("Registration error:", err);
      setError("Error al conectar con el servidor. Por favor, intente más tarde.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-header">
          <h2>Registrarse</h2>
          <button className="close-button" onClick={gohome}>
            <img src={close_icon} alt="Cerrar" />
          </button>
        </div>

        <form onSubmit={register} className="register-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="input-group">
            <div className="input-icon">
              <img src={user_icon} alt="Usuario" />
            </div>
            <input
              type="text"
              name="userName"
              placeholder="Nombre de usuario"
              value={formData.userName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <div className="input-icon">
              <img src={user_icon} alt="Nombre" />
            </div>
            <input
              type="text"
              name="firstName"
              placeholder="Nombre"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <div className="input-icon">
              <img src={user_icon} alt="Apellido" />
            </div>
            <input
              type="text"
              name="lastName"
              placeholder="Apellido"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <div className="input-icon">
              <img src={email_icon} alt="Email" />
            </div>
            <input
              type="email"
              name="email"
              placeholder="Correo electrónico"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <div className="input-icon">
              <img src={password_icon} alt="Contraseña" />
            </div>
            <input
              name="password"
              type="password"
              placeholder="Contraseña"
              value={formData.password}
              onChange={handleChange}
              required
              minLength="6"
            />
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? (
              <span className="spinner-container">
                <span className="spinner"></span> Procesando...
              </span>
            ) : "Registrarse"}
          </button>
        </form>
        
        <div className="login-link">
          ¿Ya tienes una cuenta? <a href="/login">Iniciar sesión</a>
        </div>
      </div>
    </div>
  );
};

export default Register;