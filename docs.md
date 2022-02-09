# Config

### **write**(*guild_id, option, value*)

Sets specified option in a guild's config to the given value.

### **read**(*guild_id, option*)  

Returns specified option from a guild's config. Use [fetch()](#fetch) for arrays.

### **fetch**(*guild_id, arr*) {fetch}

Returns specified array from a guild's config, spliced with the corresponding array from the global config.

### **reset**(*guild_id, option*)

Resets specified option in a guild's config to the default value.

### **append**(*guild_id, arr, value*)

Appends given value to array in a guild's config.

### **remove**(*guild_id, arr, value*)

Pops given value from array in a guild's config.

### **get**(*guild_id*)

Returns specified guild's config.

# Utils

### @**admin**()

Disallows non-admins in a guild from using an interaction.

### **jcwyt**(*member*)

Returns a boolean representing whether or not the member is on the jcwyt team.

### **load_directory**(*bot, directory_name*)

Loads every python file in a directory as a [Cog](https://nextcord.readthedocs.io/en/latest/ext/commands/cogs.html).

### **get_message**(*message, \*\*kwargs*)

Returns a message from message.yaml based on the [message specifications](#messages).

# Messages {messages}

### Reference

When selecting a message, you can use a "." to specify sections.  
For example, if you use the string "testing.foo.foobar" and your yaml file is 
```yaml
testing: # this is a section
  foo:   # this is a section in a section
    foobar: "message to send"
```
then the output would be "message to send"

### Arguments

In your message you can put "{arg}" to reference an argument. These arguments can be passed in via keyword arguments in the function.  
For example, running
```python
message = util.get_message("bar.too_young", age=17)
print(message)
```
with a yaml file
```yaml
bar:
  too_young: "Sorry, but in the United States {age} is too young to enter this establishment. You must be 18 years or older to enter."
```
will yield  
"Sorry, but in the United States 17 is too young to enter this establishment. You must be 18 years or older to enter."