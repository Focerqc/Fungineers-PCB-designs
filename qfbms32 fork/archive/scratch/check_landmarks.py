# Let's inspect landmarks in crop12_ruler.jpg:
# Top: SSRelay (U_SSR1) at X=36.7, Y=3.5. Tab is at Y~3.5
# Middle: Q1 MOSFET at X=22.4, Y=7.3.
# Middle: R001 shunt at X=23.9, Y=15.8.
# Let's check the pixel positions of Q1 and R001 in crop12_ruler.jpg

# In crop12_ruler:
# Q1 top edge is around y=650. Q1 is at Y=7.3..12.0
# Wait! In crop12_ruler, Q1's tab is at y=650..950.
# And R001 is on the right at y=650..850!
print("Mapping crop12 landmarks...")
