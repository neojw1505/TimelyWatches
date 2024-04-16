<template>
  <form>

    <div class="header-form">
      <h2>Register @ Timely Watches</h2>
    </div>

    <div class="name-fields">
      <label>First Name:</label>
      <input type="text" v-model="firstName" required />

      <div class="horizontal-space"></div>

      <label>Last Name:</label>
      <input type="text" v-model="lastName" required />

    </div>
    
      <div>
        <span v-if="firstNameError" class="error">{{ firstNameError }}</span> 
        <span v-if="lastNameError" class="error ml-4">{{ lastNameError }}</span>
      </div>

      <label>Email:</label>
      <input type="email" v-model="email" required />
      <div v-if="emailError" class="error">{{ emailError }}</div>

    <label>Living Main Address:</label>
    <input type="text" v-model="address" />

    <span>
    <label>Password:</label>
     <v-btn size="xs" class="password-toggle" @click="togglePasswordVisibility">
      {{ showPassword ? 'Hide' : 'Show' }} Password
    </v-btn>
    </span>
    <input :type="showPassword ? 'text' : 'password'" v-model="password" required />
    <div v-if="passwordError" class="error">{{ passwordError }}</div>

    <label>Phone Number:</label>
    <input type="text" v-model="phoneNumber" required pattern="[0-9]{8}" placeholder="e.g., 94204837" />
    <div v-if="phoneNumberError" class="error">{{ phoneNumberError }}</div>

    <label>Gender:</label>
    <v-select v-model="gender" :items="genders">
    </v-select>

    <label>Account Type:</label>
    <v-select v-model="accountType" :items="accountTypes" required>
    </v-select>
    <div v-if="accountTypeError" class="error">{{ accountTypeError }}</div>

    <div class="terms">
      <input type="checkbox" v-model="terms" required />
      <label>Accept Terms and Conditions</label>
    </div>
    <div v-if="termsError" class="error">{{ termsError }}</div>

    <!-- <v-dialog max-width="500" v-if="!hasErrors">
      <template v-slot:activator="{ props: activatorProps }"> -->
        <div class="submit">
            <v-btn variant="elevated" @click="handleSubmit" size="small" class="pill">Create an account</v-btn>
        </div>
      <!-- </template> -->

      <!-- <template v-slot:default="{ isActive }">
          <v-card title="Account Created">
            <v-card-text>
              Your account has beeen created, do proceed to the login form to log into your account
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                text="Close"
                @click="isActive.value = false"
              ></v-btn>
            </v-card-actions>
          </v-card>
        </template>
    </v-dialog> -->

    <!-- Error Dialog
    <v-dialog max-width="500" v-if='hasErrors'>
      <template v-slot:activator="{ props: activatorProps }">
        <div class="submit">
          <v-btn v-bind="activatorProps" variant="elevated" @click="handleSubmit" size="small" class="pill">Create an account</v-btn>
        </div>
      </template>

      <template v-slot:default="{ isActive }">
        <v-card title="Error Creating Account" color="red-lighten-5">
          <v-card-text>
            Please fix the following errors before creating your account:
            
            <ul>
              <li v-if="firstNameError" class="error">{{ firstNameError }}</li>
              <li v-if="lastNameError" class="error">{{ lastNameError }}</li>
              <li v-if="emailError" class="error">{{ emailError }}</li>
              <li v-if="passwordError" class="error">{{ passwordError }}</li>
              <li v-if="accountTypeError" class="error">{{ accountTypeError }}</li>
              <li v-if="phoneNumberError" class="error">{{ phoneNumberError }}</li>
              <li v-if="termsError" class="error">{{ termsError }}</li>
            </ul>
            
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Close" @click="isActive.value = false"></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog> -->


  </form>
</template>

<script>
import axios from 'axios'



export default {
  data() {
    return {
      email: "",
      firstName: "",
      lastName: "",
      address: "",
      password: "",
      phoneNumber: "",
      showPassword: false,
      accountType: "",
      gender: "",
      genders: ['M', 'F'],
      accountTypes: ['Buyer', 'Seller'],
      fileLink: null,
      terms: false,
      names: [],
      passwordError: "",
      firstNameError: "",
      lastNameError: "",
      emailError: "",
      phoneNumberError: "",
      accountTypeError: "",
      termsError: "",
      hasErrors: false,
    }
  },
  methods: {
    async handleSubmit() {
      // Validation of credentials
      this.passwordError = this.validatePassword(this.password)
      this.firstNameError = this.firstName.length > 0 ? 
      "" : "Please include your first name"
      this.lastNameError = this.lastName.length > 0 ?
      "" : "Please include your last name"
      this.accountTypeError = this.accountType.length > 0 ?
      "" : "Please indicate your account type"
      this.emailError = this.validateEmail(this.email)
      this.phoneNumberError = this.validatePhoneNumber(this.phoneNumber)
      this.terms ? this.termsError = "" : this.termsError = "Remember to agree to the terms"

      // Check if there are any errors
      this.hasErrors = (
        this.passwordError ||
        this.firstNameError ||
        this.lastNameError ||
        this.emailError ||
        this.accountTypeError ||
        this.phoneNumberError ||
        this.termsError
      );

      console.log(this.hasErrors)

      // If there are no errors, proceed with form submission
      if (!this.hasErrors) {
        await this.createUser();
        alert('User has been created')
      }
      else {
        alert('Check Errors for creating user')
      }


    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },

    validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return "Invalid email given, please input a valid email"
      }
      if (!(email)) {
        return "No email given, please input your email"
      }
      return ""
    },

    validatePassword(password) {
      if (password.length < 6) {
        return 'Password length must at least be 6 characters long'
      }

      // eslint-disable-next-line no-useless-escape
      const specialCharacters = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
      if (!specialCharacters.test(password)) {
        return "Passowrd must have at least one special character"
      }

      const digit = /\d/;
      if (!digit.test(password)) {
          return "Password must have at least one digit";
      }

      // Check if password contains at least one alphabet
      const alphabet = /[a-zA-Z]/;
      if (!alphabet.test(password)) {
          return "Password must have at least one alphabet";
      }

      return ""
    },

    validatePhoneNumber(phoneNum) {
      if (!phoneNum) {
        return "Phone Number is required"
      }
      else if (!/^\d{8}$/.test(phoneNum)) {
        return "Phone number must be valid"
      }
      else {
        return ""
      }
    },
    getFileLink() {
      // Access the input element using $refs
      const fileInput = this.$refs.fileInput.$el.querySelector('input[type="file"]');
      // Check if a file is selected
      if (fileInput.files.length > 0) {
        // Get the first selected file
        const file = fileInput.files[0];
        // Create a URL for the selected file
        this.fileLink = URL.createObjectURL(file);
        }
      },

    async createUser() {
  
      const params = {
          password: this.password,
          phone_number: this.phoneNumber,
          first_name: this.firstName,
          last_name: this.lastName,
          gender: this.gender,
          address: this.address,
          account_type: this.accountType,
          profile_picture: this.fileLink
        }
      
      try {
        await axios.post(`http://127.0.0.1:8000/user/${this.email}`, params);
        // Optionally, perform any actions after successful user creation
      } catch (error) {
        console.error('Error creating user:', error);
        throw error; // Re-throw the error to propagate it further
      }
    }
  }
}
</script>

<style scoped>

@font-face {
  font-family: Riviera Nights Light;
  src: url(@/styles/rivieraNights/RivieraNights-Light.otf);
}

@font-face {
  font-family: Riviera Nights Bold;
  src: url(@/styles/rivieraNights/RivieraNights-Bold.otf)
}
form {
  min-width: 500px;
  margin: 30px auto;
  background: white;
  text-align: left;
  padding: 20px;
  border-radius: 10px;
  font-family: Riviera Nights Light;
}

label {
  color: darkgray;
  display: inline-block;
  margin: 10px 0 10px;
  font-size: 0.6em;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

input, select {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}

input[type="checkbox"] {
  display:inline-block;
  width: 16px;
  margin: 0 10 0 0;
  position: relative;
  top: 2px;
}

.header-form {
  font-family: Riviera Nights Bold, sans-serif;
  margin-bottom: 10px;
}

.password-toggle {
  font-size: 12px;
  margin-left: 350px;
}

.pill {
  display: inline-block;
  margin: 20px 10px 0 0;
  padding: 6px 12px;
  background: #eee;
  border-radius: 20px;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: bold;
  color: #777;
  cursor: pointer;
}

.submit{
  text-align: center;
}

.error {
  color: #ff0062;
  margin-top: 10px;
  font-size: 0.8em;
  font-weight: bold;
}

.name-fields {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.horizontal-space {
  width: 10px; /* Adjust the width according to your preference */
}




</style>
