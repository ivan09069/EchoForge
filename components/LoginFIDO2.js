export default function LoginFIDO2() {
  return (
    <div>
      <button
        className="cosmic-btn"
        aria-describedby="biometric-status"
        disabled
      >
        Biometric login unavailable
      </button>
      <p id="biometric-status">
        This prototype does not yet implement WebAuthn authentication.
      </p>
    </div>
  );
}
