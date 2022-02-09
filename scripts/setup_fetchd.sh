# Install FetchD
git clone https://github.com/fetchai/fetchd
cd fetchd
git checkout v0.9.0
make install

# Remove FetchD git folder
cd .. && rm -rf fetchd


# Add symlink of fetchd
sudo ln -s ~/go/bin/fetchd /usr/local/bin/fetchd

# Export PATH
if [[ "$OSTYPE" == "darwin"* ]]; then
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$PATH
fi

# Clear the existing configuration
rm -rf ~/.fetchd*

# Add keys
echo "erase weekend bid boss knee vintage goat syrup use tumble device album fortune water sweet maple kind degree toss owner crane half useless sleep" |fetchd keys add validator --recover

echo "account snack twist chef razor sing gain birth check identify unable vendor model utility fragile stadium turtle sun sail enemy violin either keep fiction" | fetchd keys add bob --recover

# Start FetchD local node

# Configure node
fetchd init --chain-id=testing testing
fetchd add-genesis-account $(fetchd keys show validator -a) 100000000000000000000000stake 
fetchd add-genesis-account $(fetchd keys show bob -a) 100000000000000000000000atestfet
fetchd gentx validator 10000000000000000000000stake --chain-id testing
fetchd collect-gentxs

# Enable rest-api
sed -i '/^\[api\]$/,/^\[/ s/^enable = false/enable = true/' ~/.fetchd/config/app.toml
