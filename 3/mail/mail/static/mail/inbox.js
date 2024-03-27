document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
  const username = document.querySelector('#username').innerHTML;
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
    load_mailbox('sent');
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  username = document.querySelector('#username').innerHTML;
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails); 
    const linking = document.createElement('a');

    for (let i = 0; i < emails.length; i++) {
      recipients = emails[i].recipients;
    
      for (let j = 0; j < recipients.length; j++) {
        const email_element = document.createElement('div');
        email_element.style.border = '1px solid black';
        email_element.style.padding = '2%';

        const email_subject = document.createElement('h4');
        email_subject.innerHTML = emails[i].subject;
        email_element.append(email_subject)
  
        const email_sender = document.createElement('p');
        email_sender.innerHTML = `From: ${emails[i].sender}`;
        email_element.append(email_sender);

        const timestamp = document.createElement('p');
        timestamp.innerHTML = emails[i].timestamp;
        email_element.append(timestamp);

        if (emails[i].read) {
          email_element.style.background = 'grey';
        } else {
          email_element.style.background = 'white';
        }
        
        email_element.addEventListener('click', () => view_email(emails[i].id))
        
        const emails_view = document.querySelector('#emails-view');
        emails_view.append(email_element);
      }
    }
  }); 
}


function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';

  document.querySelector('#view-email').innerHTML = '';

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  

  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    const email_element = document.querySelector('#view-email');

    add_element(parent_element=email_element, new_element_tag='h1', innerHTML=email.subject);

    add_element(parent_element=email_element, new_element_tag='h3', innerHTML=email.sender);

    add_element(parent_element=email_element, new_element_tag='p', innerHTML=email.timestamp);

    email_element.append(document.createElement('br'));
    if (email.sender != username) {
      const button = add_element(parent_element=email_element, new_element_tag='button');
      button.id = 'archive_button';
      if (email.archived === true) {
        button.innerHTML = 'unarchive';
        
      } else {
        button.innerHTML = 'archive';
      }
      button.addEventListener('click', () => archive(id=email.id, archived=email.archived));
    }

    email_element.append(document.createElement('br'));

    add_element(parent_element=email_element, new_element_tag='p', innerHTML=`From: ${email.body}`);

    const reply_button = document.createElement('button');
    reply_button.innerHTML = 'Reply';
    reply_button.addEventListener('click', () => reply(email.id));
    email_element.append(reply_button);
  });
}


function add_element(parent_element, new_element_tag, innerHTML='') {
  const new_element = document.createElement(new_element_tag);
  new_element.innerHTML = innerHTML;
  parent_element.append(new_element);
  return new_element;
}

function archive(id, archived) {
  archived = !archived;
  const button = document.querySelector('#archive_button');
  if (button.innerHTML === 'archive') {
    button.innerHTML = 'unarchive';
  } else {
    button.innerHTML = 'archive';
  }

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archived
    })
  })
}


function reply(id) {
  compose_email();

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const subject = email.subject;
    const sender = email.sender;
    const timestamp = email.timestamp;
    const body = email.body;
    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
    document.querySelector('#compose-body').value = `${sender} wrote on ${timestamp}: \n${body}`;
  })

  
}