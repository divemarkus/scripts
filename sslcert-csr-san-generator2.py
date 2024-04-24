from OpenSSL import crypto

def generate_csr(common_name, san_list, organization_name, organization_unit_name, city_name, state_name, country_name, email_address):
  """
  Generates an SSL certificate signing request (CSR) with the provided details.

  Args:
      common_name: The primary domain name for the certificate.
      san_list: A list of additional subject alternative names (SANs).
      organization_name: The organization name.
      organization_unit_name: The organization unit name (optional).
      city_name: The city name.
      state_name: The state name.
      country_name: The two-letter country code (e.g., US).
      email_address: The email address associated with the certificate.

  Returns:
      A PEM-encoded string containing the CSR.
  """

  # Create a key pair
  key = crypto.PKey()
  key.generate_key(crypto.TYPE_RSA, 2048)

  # Create a new CSR object
  csr = crypto.X509Req()

  # Set the subject
  subject = csr.get_subject()
  subject.CN = common_name
  subject.O = organization_name
  subject.OU = organization_unit_name
  subject.L = city_name
  subject.ST = state_name
  subject.C = country_name
  subject.emailAddress = email_address

  # Add subject alternative names (SANs)
  for san in san_list:
    subject_alt_name = crypto.X509ExtensionSubjectAltName()
    subject_alt_name.add_dns(san)
    csr.add_extensions([subject_alt_name])

  # Set the public key
  csr.set_pubkey(key)

  # Sign the CSR with the private key
  csr.sign(key, crypto.Hash.SHA256())

  # Return the CSR as a PEM-encoded string
  return crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr)

# Example usage (**moved outside the function definition**)
common_name = "your_domain.com"
san_list = ["www.your_domain.com", "mail.your_domain.com"]
organization_name = "Your Organization Name"
organization_unit_name = "IT Department"  # Optional
city_name = "Your City"
state_name = "Your State"
country_name = "US"
email_address = "admin@your_domain.com"

csr_pem = generate_csr(common_name, san_list, organization_name, organization_unit_name, city_name, state_name, country_name, email_address)

# Save the CSR to a file
with open("your_domain.csr", "wb") as f:
  f.write(csr_pem)

print("CSR generated and saved to your_domain.csr")
