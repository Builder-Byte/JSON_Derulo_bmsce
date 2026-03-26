from backend.services.state_manager import StateManager

sm = StateManager()

# --- Update: Add entries for users ---
print("=== update() ===")

out1 = sm.update("alice", {"role": "user", "text": "Hello!"})
print(f"alice after 1st update : {out1}")

out2 = sm.update("alice", {"role": "bot", "text": "Hi Alice!"})
print(f"alice after 2nd update : {out2}")

out3 = sm.update("bob", {"role": "user", "text": "Hey there."})
print(f"bob   after 1st update : {out3}")

# --- get_history: Full history for a user ---
print("\n=== get_history() ===")

print(f"alice history : {sm.get_history('alice')}")
print(f"bob   history : {sm.get_history('bob')}")
print(f"carol history : {sm.get_history('carol')}")   # user doesn't exist

# --- get_userID: Raw store entry for a user ---
print("\n=== get_userID() ===")

print(f"alice : {sm.get_userID('alice')}")
print(f"carol : {sm.get_userID('carol')}")    
